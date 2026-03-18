import time
import pytest
from engine import (
    create_engine,
    connect,
    EngineOptions,
    ConnectionCapability,
    KeyInputEnum,
    InputStateEnum,
    InputEvent,
)
from engine.domains.input import InputProvider, InputManager


class MockKeyboard(InputProvider):
    """Simulates raw hardware signals for the integration test."""

    def __init__(self):
        self.mock_events: list[InputEvent] = []

    def poll(self):
        events = list(self.mock_events)
        self.mock_events.clear()
        return events


def test_developer_input_workflow():
    # Initialization
    options = EngineOptions(use_input=True)
    engine = create_engine(options)

    api = connect(
        engine,
        [
            ConnectionCapability.INPUT,
            ConnectionCapability.EVENTS,
            ConnectionCapability.SYSTEM,
        ],
    )

    input_manager = engine.get_manager("input", InputManager)
    if input_manager is None:
        pytest.fail("InputManager was not registered in the engine.")

    keyboard = MockKeyboard()
    input_manager.add_provider(keyboard)

    # 1. Test State Polling
    keyboard.mock_events.append(
        InputEvent(
            identifier=KeyInputEnum.SPACE,  # Updated field name
            state=InputStateEnum.PRESSED,
            timestamp=time.time(),
        )
    )

    # Pulse to poll and update internal manager state
    engine.update()
    assert api.input.is_pressed(KeyInputEnum.SPACE) is True

    # 2. Test Event Subscription
    received_event = False

    def on_space_pressed(event):
        nonlocal received_event
        received_event = True

    api.events.on(KeyInputEnum.SPACE, on_space_pressed)

    # Trigger a new hardware event
    keyboard.mock_events.append(
        InputEvent(
            identifier=KeyInputEnum.SPACE,
            state=InputStateEnum.PRESSED,
            timestamp=time.time(),
        )
    )

    # Pulse 1: Manager polls -> bus.emit(EventData(name=KeyInputEnum.SPACE, ...))
    # Event lands in _next_queue
    engine.update()

    # Pulse 2: Bus.process() swaps queues -> executes on_space_pressed
    engine.update()
    assert received_event is True

    # 3. Test Telemetry
    metrics = api.input.get_metrics()
    assert metrics is not None
    assert metrics.total_events_processed >= 1
    assert metrics.active_keys_count == 1

    # 4. Test Synthetic Decay
    # Force clock back to simulate 200ms passing since last update
    engine.clock.last_time -= 0.2
    engine.update()  # Triggers _handle_key_decay
    engine.update()  # Process the synthetic RELEASED event

    assert api.input.is_pressed(KeyInputEnum.SPACE) is False

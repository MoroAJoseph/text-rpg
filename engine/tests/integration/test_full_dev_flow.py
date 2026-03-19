import time
import pytest
from enum import Enum, auto
from dataclasses import dataclass
from unittest.mock import MagicMock, patch

# Core & Config Imports
from engine.core.bus import EventBus
from engine.core.models import EventData
from engine.core.enums import EventTypeEnum
from engine.config.models import (
    EngineConfig,
    InputConfig,
    InputCapabilities,
    CapabilityConfig,
    KeyboardParameters,
)
from engine.kernel.engine import Engine
from engine.api.factory import connect
from engine.core.domain_protocols import DomainManager

# Domain Imports
from engine.domains.input.enums import KeyInputEnum, InputStateEnum
from engine.domains.input.models import InputEvent, InputPayload
from engine.domains.input.manager import InputManager

# --- 1. CUSTOM DOMAIN DEFINITIONS ---


class CombatAction(Enum):
    STRIKE = auto()
    BLOCK = auto()


@dataclass
class CombatBus(EventBus):
    """Custom bus for domain-specific actions."""

    def __post_init__(self):
        super().__init__()


class CombatManager(DomainManager):
    """Manager that reacts to Input via the API and emits Combat actions."""

    def __init__(self, bus: CombatBus):
        self.bus = bus
        self.actions_logged = []

    def register_bus(self, bus: EventBus) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def execute_strike(self, power: int):
        self.actions_logged.append(f"STRIKE_{power}")
        self.bus.emit(
            EventData(type=EventTypeEnum.SYSTEM, name=CombatAction.STRIKE, data=power)
        )


# --- 2. THE INTEGRATION TEST ---


def test_full_engine_dev_flow():
    # STEP A: CONFIGURATION
    kb_params = KeyboardParameters(raw_mode=True)
    kb_config = CapabilityConfig(driver="mock", enabled=True, parameters=kb_params)
    input_caps = InputCapabilities(keyboard=kb_config)

    config = EngineConfig(
        tick_rate=60,
        input=InputConfig(
            enabled=True,
            decay_threshold=0.1,
            capabilities=input_caps,
        ),
    )

    # STEP B: KERNEL INITIALIZATION
    with patch("engine.kernel.engine.Engine._bootstrap_domains"):
        engine = Engine(config)

    # STEP C: DOMAIN REGISTRATION
    # Managers MUST be in registry before connect()
    input_manager = InputManager(config.input)
    input_manager.register_bus(engine.ctx.bus)
    engine.managers.add("input", input_manager)

    combat_bus = CombatBus()
    combat_mgr = CombatManager(combat_bus)
    engine.managers.add("combat", combat_mgr)

    # STEP D: API CONNECTION
    api = connect(engine)

    # Attach mock driver
    mock_hw = MagicMock()
    input_manager.add_spoke("mock_driver", mock_hw, 60.0)

    # STEP E: USERLAND LOGIC
    combat_events_received = []

    def on_input(event: EventData):
        # 1. Type Guard: Check if data is present
        if event.data is None:
            return

        # 2. Assign with confidence
        payload: InputPayload = event.data

        # 3. Filter for Space + Pressed
        if (
            payload.identifier == KeyInputEnum.SPACE
            and payload.state == InputStateEnum.PRESSED
        ):
            combat_mgr.execute_strike(power=9001)

    # Subscribe to the core INPUT type on the engine bus
    engine.ctx.bus.subscribe_to_type(EventTypeEnum.INPUT, on_input)

    combat_bus.subscribe_to_name(
        CombatAction.STRIKE, lambda e: combat_events_received.append(e.data)
    )

    # STEP F: THE 3-FLUSH CYCLE
    # Cycle 1: Poll Hardware -> engine.bus._next_queue
    # Cycle 2: engine.bus.process() -> trigger on_space_pressed -> combat_bus._next_queue

    mock_hw.poll.return_value = [
        InputPayload(
            identifier=KeyInputEnum.SPACE,
            state=InputStateEnum.PRESSED,
            timestamp=time.perf_counter(),
            raw_data=" ",
            coords=(0, 0),
        )
    ]

    engine.update()  # Tick 1
    engine.update()  # Tick 2 (Triggering callbacks)
    engine.update()  # Tick 3 (Settling state)

    # STEP G: VERIFICATION
    assert api.input is not None
    assert api.input.is_down(KeyInputEnum.SPACE) is True

    # Verify Custom Bus (Manual process since it's not managed by Engine)
    combat_bus.process()

    assert "STRIKE_9001" in combat_mgr.actions_logged
    assert 9001 in combat_events_received

    # STEP H: TEMPORAL DECAY
    # Simulate 0.2s passing (Threshold 0.1)
    with patch.object(engine.clock, "tick", return_value=0.2):
        mock_hw.poll.return_value = []
        engine.update()  # Decay logic -> Emits Release
        engine.update()  # Bus Flush -> Updates API state

    assert api.input.is_down(KeyInputEnum.SPACE) is False

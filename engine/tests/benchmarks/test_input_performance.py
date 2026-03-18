import time
from engine import create_engine, EngineOptions
from engine.domains.input import InputEvent, InputStateEnum, KeyInputEnum, InputManager


def test_input_normalization_overhead(benchmark):
    engine = create_engine(EngineOptions(use_input=True))

    # Pass the expected type to satisfy Pylance and the runtime check
    input_manager = engine.get_manager("input", InputManager)

    if input_manager is None:
        raise RuntimeError("InputManager not found")

    raw_event = InputEvent(
        identifier=KeyInputEnum.SPACE,
        state=InputStateEnum.PRESSED,
        timestamp=time.time(),
    )

    def normalize_and_emit():
        input_manager._process_input(raw_event)
        # Prevent queue bloat during benchmarking
        engine.ctx.bus._next_queue.clear()

    benchmark(normalize_and_emit)

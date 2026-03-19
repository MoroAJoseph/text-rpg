import time
from dataclasses import asdict
from engine.config.models import EngineConfig, InputConfig
from engine.domains.input.enums import InputStateEnum, KeyInputEnum
from engine.domains.input.manager import InputManager
from engine.domains.input.models import InputPayload
from engine.kernel.factory import create_engine


def test_input_normalization_overhead(benchmark):
    config_obj = EngineConfig(input=InputConfig(enabled=True))
    config = asdict(config_obj)
    engine = create_engine(config)

    input_manager = engine.managers.get("input", InputManager)
    if not input_manager:
        raise RuntimeError("InputManager not found")

    payload = InputPayload(
        identifier=KeyInputEnum.SPACE,
        state=InputStateEnum.PRESSED,
        timestamp=time.time(),
        raw_data=" ",
        coords=(0, 0),
    )

    def normalize_and_emit():
        input_manager._process_input(payload)
        engine.ctx.bus._next_queue.clear()

    benchmark(normalize_and_emit)

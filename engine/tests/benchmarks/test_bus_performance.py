import pytest
from dataclasses import asdict
from engine.config.models import EngineConfig
from engine.core.models import EventData
from engine.core.enums import EventTypeEnum, SystemEventEnum
from engine.kernel.factory import create_engine


@pytest.mark.parametrize("count", [100, 1000, 100000])
def test_bus_throughput(benchmark, count):
    config = asdict(EngineConfig(tick_rate=60))
    engine = create_engine(config)
    bus = engine.ctx.bus
    bus.subscribe_to_name(SystemEventEnum.MAIN_TICK, lambda e: None)

    def emit_and_process():
        for _ in range(count):
            bus.emit(
                EventData(type=EventTypeEnum.SYSTEM, name=SystemEventEnum.MAIN_TICK)
            )
        bus.process()

    benchmark(emit_and_process)

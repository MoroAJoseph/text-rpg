from dataclasses import asdict
from engine.config.models import EngineConfig
from engine.core.enums import EventTypeEnum, SystemEventEnum
from engine.core.models import EventData
from engine.kernel.factory import create_engine


def test_event_allocation_cost(benchmark):
    config = asdict(EngineConfig(tick_rate=60))
    engine = create_engine(config)
    bus = engine.ctx.bus

    def allocate_and_emit():
        bus.emit(EventData(type=EventTypeEnum.SYSTEM, name=SystemEventEnum.MAIN_TICK))

    benchmark(allocate_and_emit)


def test_event_reuse_cost(benchmark):
    config = asdict(EngineConfig(tick_rate=60))
    engine = create_engine(config)
    bus = engine.ctx.bus
    static_event = EventData(type=EventTypeEnum.SYSTEM, name=SystemEventEnum.MAIN_TICK)

    def reuse_and_emit():
        bus.emit(static_event)

    benchmark(reuse_and_emit)

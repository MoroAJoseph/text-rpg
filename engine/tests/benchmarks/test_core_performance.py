from dataclasses import asdict
from engine.config.models import EngineConfig
from engine.core.enums import EventTypeEnum, SystemEventEnum
from engine.core.models import EventData
from engine.kernel.factory import create_engine


def test_bus_dispatch_scaling(benchmark):
    config = asdict(EngineConfig(tick_rate=60))
    engine = create_engine(config)
    bus = engine.ctx.bus
    event = EventData(type=EventTypeEnum.SYSTEM, name=SystemEventEnum.MAIN_TICK)
    bus.subscribe_to_name(SystemEventEnum.MAIN_TICK, lambda e: None)

    def dispatch():
        bus._current_queue.append(event)
        bus.process()

    benchmark(dispatch)


def test_engine_empty_update_cycle(benchmark):
    config = asdict(EngineConfig(tick_rate=60))
    engine = create_engine(config)
    benchmark(engine.update)

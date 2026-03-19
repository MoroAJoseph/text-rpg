from dataclasses import asdict
from engine.config.models import EngineConfig
from engine.core.enums import SystemEventEnum
from engine.api.factory import connect
from engine.kernel.factory import create_engine


def test_api_to_bus_latency(benchmark):
    # Convert dataclass to dict for create_engine compatibility
    config = asdict(EngineConfig(tick_rate=60))
    engine = create_engine(config)
    api = connect(engine)

    def full_stack_cycle():
        api.system.stop()
        engine.ctx.bus.process()

    benchmark(full_stack_cycle)


def test_api_subscription_latency(benchmark):
    config = asdict(EngineConfig(tick_rate=60))
    engine = create_engine(config)
    api = connect(engine)

    def api_subscribe():
        api.events.on(SystemEventEnum.MAIN_TICK, lambda e: None)
        engine.ctx.bus._listeners.clear()

    benchmark(api_subscribe)

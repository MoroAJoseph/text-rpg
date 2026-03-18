import pytest
from engine import create_engine, EventData, EventTypeEnum, SystemEventEnum


def test_bus_throughput(benchmark):
    engine = create_engine()
    bus = engine.ctx.bus

    # Pre-subscribe to eliminate lookup overhead from the measurement
    bus.subscribe(SystemEventEnum.ENGINE_TICK, lambda e: None)

    def emit_and_process():
        # Emit 100 events
        for _ in range(100):
            bus.emit(
                EventData(type=EventTypeEnum.SYSTEM, name=SystemEventEnum.ENGINE_TICK)
            )
        # Process the batch
        bus.process()

    # The benchmark will run this thousands of times to get an average
    benchmark(emit_and_process)

from engine import create_engine, EventData, EventTypeEnum, SystemEventEnum


def test_event_allocation_cost(benchmark):
    """Benchmark the cost of creating a new EventData instance vs just emitting."""
    bus = create_engine().ctx.bus

    def allocate_and_emit():
        bus.emit(EventData(type=EventTypeEnum.SYSTEM, name=SystemEventEnum.ENGINE_TICK))

    benchmark(allocate_and_emit)


def test_event_reuse_cost(benchmark):
    """Benchmark emitting a pre-allocated static event."""
    bus = create_engine().ctx.bus
    static_event = EventData(
        type=EventTypeEnum.SYSTEM, name=SystemEventEnum.ENGINE_TICK
    )

    def reuse_and_emit():
        bus.emit(static_event)

    benchmark(reuse_and_emit)

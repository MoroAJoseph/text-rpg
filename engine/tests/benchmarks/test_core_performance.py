from engine import (
    create_engine,
    SystemEventEnum,
    EventData,
    EventTypeEnum,
    EngineOptions,
)


def test_bus_dispatch_scaling(benchmark):
    """
    Measures the cost of routing a single event to a single listener.
    This isolates the overhead of _get_event_name and dictionary lookups.
    """

    engine = create_engine()
    bus = engine.ctx.bus

    # Static data to avoid allocation overhead during the loop
    event = EventData(type=EventTypeEnum.SYSTEM, name=SystemEventEnum.ENGINE_TICK)
    bus.subscribe(SystemEventEnum.ENGINE_TICK, lambda e: None)

    def dispatch():
        # Directly populate current queue to skip the swap overhead
        bus._current_queue.append(event)
        bus.process()

    benchmark(dispatch)


def test_engine_empty_update_cycle(benchmark):
    """
    Measures the baseline cost of engine.update().

    This includes:
    - Clock ticking and DT calculation.
    - Bus queue swapping and empty processing.
    - ManagerRegistry iteration.
    - Emission of the SystemEventEnum.ENGINE_TICK packet.
    """
    # Use a clean engine with no extra managers to find the 'floor'
    options = EngineOptions(use_input=False)
    engine = create_engine(options)

    # We benchmark the update call directly
    benchmark(engine.update)

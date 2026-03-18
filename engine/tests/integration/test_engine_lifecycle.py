from engine import (
    create_engine,
    EngineOptions,
    SystemEventEnum,
    ConnectionCapability,
    connect,
)


def test_engine_tick_propagation():
    engine = create_engine(EngineOptions(use_input=False))
    api = connect(engine, [ConnectionCapability.EVENTS])

    tick_count = 0

    def count_ticks(event):
        nonlocal tick_count
        tick_count += 1

    # Subscribe
    api.events.on(SystemEventEnum.ENGINE_TICK, count_ticks)

    # Pulse the engine
    engine.update()  # Emits
    engine.update()  # Processes

    assert tick_count >= 1

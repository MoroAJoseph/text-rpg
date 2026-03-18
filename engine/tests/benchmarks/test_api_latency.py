from engine import create_engine, connect, ConnectionCapability, SystemEventEnum


def test_api_to_bus_latency(benchmark):
    engine = create_engine()
    api = connect(engine, [ConnectionCapability.SYSTEM, ConnectionCapability.EVENTS])

    def full_stack_cycle():
        api.system.start()
        engine.ctx.bus.process()

    benchmark(full_stack_cycle)


def test_api_subscription_latency(benchmark):
    """Measures the overhead of the API wrapper versus direct Bus access."""
    engine = create_engine()
    api = connect(engine, [ConnectionCapability.EVENTS])

    def api_subscribe():
        api.events.on(SystemEventEnum.ENGINE_TICK, lambda e: None)
        # Clear listeners to prevent memory bloat during benchmark rounds
        engine.ctx.bus._listeners.clear()

    benchmark(api_subscribe)

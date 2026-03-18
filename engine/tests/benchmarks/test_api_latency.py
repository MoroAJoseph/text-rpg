from engine import create_engine, connect, ConnectionCapability, SystemEventEnum


def test_api_to_bus_latency(benchmark):
    engine = create_engine()
    api = connect(engine, [ConnectionCapability.SYSTEM, ConnectionCapability.EVENTS])

    def full_stack_cycle():
        api.system.start()
        engine.ctx.bus.process()

    benchmark(full_stack_cycle)

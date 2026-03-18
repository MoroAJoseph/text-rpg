from engine import create_engine, connect, EngineOptions, ConnectionCapability, Engine


def test_engine_initialization():
    engine = create_engine(EngineOptions(width=100))
    assert isinstance(engine, Engine)
    assert engine.options.width == 100
    assert engine.ctx is not None
    assert engine.ctx.bus is not None


def test_connect_scopes_apis():
    engine = create_engine()
    # Request specific handles
    api = connect(engine, [ConnectionCapability.SYSTEM, ConnectionCapability.EVENTS])

    assert hasattr(api, "system")
    assert hasattr(api, "events")
    # Should not exist if not requested
    assert not hasattr(api, "input")


def test_api_connection_injection():
    engine_a = create_engine()
    api_a = connect(engine_a, [ConnectionCapability.SYSTEM])
    # Verify the API is looking at the correct instance bus
    assert api_a.system._bus is engine_a.ctx.bus

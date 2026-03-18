from engine import create_engine, ConnectionCapability, connect


def test_api_to_engine_shutdown_flow():
    # Setup engine and APIs
    engine = create_engine()
    api = connect(engine, [ConnectionCapability.SYSTEM, ConnectionCapability.EVENTS])

    # Trigger stop via the Developer API
    api.system.shutdown()

    # Manually process the frame
    # Frame A: API emits STOP -> Bus captures it
    engine.update()

    # Verify the callback was hit and engine.running flipped
    assert engine.ctx.running is False

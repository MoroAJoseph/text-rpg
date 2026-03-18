from engine import create_engine


def test_engine_stops_on_signal():
    engine = create_engine()
    engine.ctx.running = True

    # Simulate the exit signal being received
    engine._handle_exit_signal(None)

    assert engine.ctx.running is False

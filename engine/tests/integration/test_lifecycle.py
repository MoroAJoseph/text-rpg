def test_system_stop_integration(test_env):
    engine, api = test_env
    engine.ctx.running = True

    # 1. API Call
    api.system.stop()

    # 2. Kernel Update
    # Flush 1: Process() picks up STOP event
    # _handle_exit() sets engine.ctx.running = False
    engine.update()

    assert engine.ctx.running is False

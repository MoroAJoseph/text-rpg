from engine import create_engine, CTX
from engine.core import EngineEventBus


def test_ctx_singleton_behavior():
    """Verify CTX points to the active engine's bus and state."""
    # 1. Initialize Engine
    engine = create_engine()

    # 2. Check if CTX is wired to this engine's unique instances
    assert CTX.bus == engine.ctx.bus
    assert isinstance(CTX.bus, EngineEventBus)

    # 3. Verify state synchronization
    engine.ctx.running = True
    assert CTX.running is True

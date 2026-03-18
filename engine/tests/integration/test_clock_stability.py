import time
from engine import create_engine


def test_engine_dt_consistency():
    engine = create_engine()

    # First frame
    engine.update()

    # Force a delay to simulate heavy processing
    time.sleep(0.05)

    # Second frame
    engine.update()

    # Engine clock should report a dt of ~0.05s
    assert engine.clock.dt >= 0.05

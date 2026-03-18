import time
from engine.core import Clock


def test_clock_delta_calculation():
    # Set high FPS to minimize sleep interference
    clock = Clock(target_fps=120)

    # First tick initializes last_time
    clock.tick()
    time.sleep(0.02)
    dt = clock.tick()

    # dt should be roughly 0.02s
    assert 0.015 < dt < 0.03


def test_clock_framerate_capping():
    fps = 60
    clock = Clock(target_fps=fps)
    expected_dt = 1.0 / fps

    clock.tick()
    dt = clock.tick()

    # Clock should have slept to meet the 16.6ms requirement
    # We check that it isn't significantly faster than the limit
    assert dt >= expected_dt * 0.95

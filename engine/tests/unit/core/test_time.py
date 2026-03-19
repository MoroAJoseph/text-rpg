import time
from engine.core.time import Clock


def test_clock_framerate_capping():
    rate = 60
    clock = Clock(target_tick_rate=rate)
    expected_dt = 1.0 / rate

    clock.tick()
    dt = clock.tick()

    # Should sleep to maintain the 16.6ms frame time
    assert dt >= expected_dt * 0.9


def test_clock_dt_calculation():
    clock = Clock(target_tick_rate=60)

    # Initialize
    clock.tick()
    time.sleep(0.01)
    dt = clock.tick()

    assert 0.009 <= dt <= 0.02


def test_tick_rate_property():
    clock = Clock(target_tick_rate=100)
    clock.dt = 0.01  # Simulate 100Hz
    assert clock.tick_rate == 100.0

    clock.dt = 0  # Prevent division by zero
    assert clock.tick_rate == 0.0

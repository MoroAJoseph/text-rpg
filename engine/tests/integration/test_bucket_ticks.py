from unittest.mock import MagicMock, patch
from engine.core.enums import SystemEventEnum


def test_custom_tick_buckets(test_env):
    engine, api = test_env

    # 1. Configuration
    engine.config.rates["slow_tick"] = 10.0
    # Ensure the bucket exists in the engine's internal state
    engine._buckets["slow_tick"] = MagicMock(accumulator=0.0, interval=0.1)

    # 2. Subscription
    events = []
    # Note: Ensure the API handler correctly receives the EventData object
    api.events.on(SystemEventEnum.CUSTOM_TICK, lambda e: events.append(e))

    # 3. Simulate Time & Update
    with patch.object(engine.clock, "tick", return_value=0.11):
        # First update: Triggers the bucket logic -> emits to 'next_queue'
        engine.update()

        # Second update: Flushes 'next_queue' to 'current_queue' -> dispatches to listener
        engine.update()

    # 4. Verification
    assert len(events) >= 1
    # Accessing the payload via the .data attribute of the EventData
    assert events[0].data["label"] == "slow_tick"

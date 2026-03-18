from unittest.mock import MagicMock

from engine.domains.input import InputTelemetry


def test_telemetry_accumulation():
    bus = MagicMock()
    telemetry = InputTelemetry(bus)

    telemetry.record_poll(0.0, 5)  # Processed 5 events
    telemetry.record_poll(0.0, 3)  # Processed 3 events

    assert telemetry.metrics.total_events_processed == 8


def test_telemetry_state_update():
    bus = MagicMock()
    telemetry = InputTelemetry(bus)

    telemetry.update_state(12)
    assert telemetry.metrics.active_keys_count == 12

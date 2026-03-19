import time
from unittest.mock import MagicMock
from engine.domains.input.telemetry import InputTelemetry


def test_telemetry_reporting_interval():
    bus = MagicMock()
    # Set a very short interval for testing
    telemetry = InputTelemetry(bus, report_interval=0.01)

    telemetry.record_poll(time.perf_counter(), 5)
    time.sleep(0.02)
    telemetry.record_poll(time.perf_counter(), 2)

    # Should have emitted a TelemetryEvent once
    assert bus.emit.called

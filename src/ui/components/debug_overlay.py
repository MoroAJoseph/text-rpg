# src/ui/components/debug_overlay.py

import threading
import time
from src.runtime.core.event_bus import EVENT_BUS
from src.models.type_models import (
    UIActionsEnum,
    Event,
    EventTypeEnum,
    UIEventsEnum,
)
from .overlay import UIOverlay
from .buffer import UIBuffer


class DebugOverlay(UIOverlay):
    """Overlay for real-time engine telemetry and debug info with auto-refresh."""

    def __init__(self, refresh_hz: int = 10):
        # No longer taking telemetry as an argument
        self.refresh_interval = 1.0 / refresh_hz

        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._refresh_loop, daemon=True)
        self._thread.start()

    def _refresh_loop(self):
        """Background thread to pulse render events for live telemetry."""
        while not self._stop_event.is_set():
            EVENT_BUS.emit(Event(type=EventTypeEnum.UI, name=UIEventsEnum.RENDER))
            time.sleep(self.refresh_interval)

    def stop(self):
        self._stop_event.set()
        if self._thread.is_alive():
            self._thread.join(timeout=0.1)

    def draw(self, buffer: UIBuffer):
        """Draws the telemetry box using the global TELEMETRY_MANAGER."""
        from src.runtime.managers.telemetry import TELEMETRY_MANAGER

        stats = TELEMETRY_MANAGER.data

        width = 26
        height = 8
        start_x = buffer.width - width - 1
        start_y = 1

        self._draw_box(buffer, start_x, start_y, width, height)

        # Formatting with strict None checks
        fps_val = f"{stats.fps:6.1f}" if stats.fps is not None else "---.-"
        lat_val = (
            f"{stats.latency_ms:6.2f}" if stats.latency_ms is not None else "---.--"
        )
        key_val = str(stats.last_key)[:12] if stats.last_key else "None"

        # Ensure mouse_pos isn't None before indexing
        if stats.mouse_pos and len(stats.mouse_pos) == 2:
            mouse_val = f"{stats.mouse_pos[0]:3},{stats.mouse_pos[1]:3}"
        else:
            mouse_val = "  0,  0"

        # Content Rendering
        buffer.write(start_x + 2, start_y + 1, "── Debug Telemetry ──")
        buffer.write(start_x + 2, start_y + 2, f"FPS:      {fps_val}")
        buffer.write(start_x + 2, start_y + 3, f"LATENCY:  {lat_val}ms")
        buffer.write(start_x + 2, start_y + 4, f"LAST KEY: {key_val}")
        buffer.write(start_x + 2, start_y + 5, f"MOUSE:    {mouse_val}")
        buffer.write(
            start_x + 2, start_y + 6, f"HITBOXES: {stats.active_hitboxes or 0}"
        )

    def handle_action(self, action: UIActionsEnum) -> bool:
        return False

    def _draw_box(self, buffer: UIBuffer, x: int, y: int, w: int, h: int):
        buffer.write(x, y, "┌" + "─" * (w - 2) + "┐")
        for i in range(1, h - 1):
            buffer.write(x, y + i, "│" + " " * (w - 2) + "│")
        buffer.write(x, y + h - 1, "└" + "─" * (w - 2) + "┘")

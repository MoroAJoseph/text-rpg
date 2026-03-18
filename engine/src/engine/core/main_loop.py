import time
from .app_context import CTX


class MainLoop:
    def __init__(self, target_fps: int = 60):
        self.target_fps = target_fps
        self.frame_duration = 1.0 / target_fps
        self.log = CTX.system_log

    def run(self):
        """The core engine cycle."""
        self.log.info(f"Starting Engine Main Loop at {self.target_fps} FPS")

        while CTX.running:
            frame_start = time.perf_counter()

            # 1. Input Phase
            if CTX.input:
                CTX.input.update()

            # 2. Logic Phase (Process Event Bus)
            CTX.bus.process()

            # 3. Render Phase
            if CTX.renderer:
                CTX.renderer.render()

            # 4. Telemetry & Sync Phase
            frame_end = time.perf_counter()
            frame_time = frame_end - frame_start

            # Update Telemetry Stats
            if CTX.telemetry:
                fps = 1.0 / frame_time if frame_time > 0 else 0
                CTX.telemetry.update_metric("fps", round(fps, 2))
                CTX.telemetry.update_metric(
                    "frame_time_ms", round(frame_time * 1000, 4)
                )

            # Sleep to maintain target FPS
            sleep_time = self.frame_duration - frame_time
            if sleep_time > 0:
                time.sleep(sleep_time)

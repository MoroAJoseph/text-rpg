import time


class Clock:
    def __init__(self, target_fps: int = 60):
        self.target_fps = target_fps
        self.frame_duration = 1.0 / target_fps
        self.last_time = time.perf_counter()
        self.dt = 0.0

    def tick(self) -> float:
        """Calculates delta time and caps the frame rate."""
        now = time.perf_counter()
        self.dt = now - self.last_time

        # Frame limiting logic
        sleep_time = self.frame_duration - self.dt
        if sleep_time > 0:
            time.sleep(sleep_time)
            now = time.perf_counter()
            self.dt = now - self.last_time

        self.last_time = now
        return self.dt

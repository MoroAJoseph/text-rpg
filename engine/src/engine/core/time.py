import time


class Clock:
    def __init__(self, target_tick_rate: int = 60):
        self.target_tick_rate = target_tick_rate
        self.tick_duration = 1.0 / target_tick_rate
        self.last_time = time.perf_counter()
        self.dt = 0.001

    @property
    def tick_rate(self) -> float:
        return 1.0 / self.dt if self.dt > 0 else 0.0

    def tick(self) -> float:
        now = time.perf_counter()
        self.dt = now - self.last_time

        sleep_time = self.tick_duration - self.dt
        if sleep_time > 0:
            time.sleep(sleep_time)
            now = time.perf_counter()
            self.dt = now - self.last_time

        self.last_time = now
        return self.dt

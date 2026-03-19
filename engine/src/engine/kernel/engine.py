from typing import Dict

from ..core.enums import EventTypeEnum, SystemEventEnum
from ..core.models import EventData, TickBucket
from ..core.time import Clock
from ..config.models import EngineConfig
from .context import CTX
from .registry import ManagerRegistry


class Engine:
    """The Root Kernel. Orchestrates DomainManagers via the 3-Flush Cycle."""

    def __init__(self, config: EngineConfig):
        self.config = config
        self.ctx = CTX
        self.managers = ManagerRegistry()
        self.clock = Clock(target_tick_rate=config.tick_rate)

        # Multi-rate buckets for logic outside the main tick
        self._buckets: Dict[str, TickBucket] = {
            name: TickBucket(name=name, target_rate=rate)
            for name, rate in self.config.rates.items()
        }

        self._bootstrap_domains()

        # Subscribe to termination signals
        self.ctx.bus.subscribe_to_name(SystemEventEnum.STOP, self._handle_exit)

    def _bootstrap_domains(self):

        # Input
        if self.config.input and self.config.input.enabled:
            from ..domains.input.registry import resolve_input_domain

            # Input Manager
            manager = resolve_input_domain(self.config.input)
            manager.register_bus(self.ctx.bus)

            self.managers.add("input", manager)

        # TODO: Audio

        # TODO: Display

    def run(self):
        self.ctx.running = True
        try:
            while self.ctx.running:
                self.update()
        except KeyboardInterrupt:
            self.ctx.exit_code = 130
        finally:
            self._shutdown()

    def update(self):
        """The 3-Flush Cycle: Poll -> Sync -> Dispatch."""
        dt = self.clock.tick()

        # FLUSH 1: Clear previous frame's artifacts
        self.ctx.bus.process()

        # STEP A: Manager Updates (Drivers poll hardware here)
        for manager in self.managers.values():
            manager.update(dt)

        # FLUSH 2: Synchronize State (Managers emit events to the bus)
        self.ctx.bus.process()

        # STEP B: System/Fixed Ticks
        self._process_buckets(dt)
        self.ctx.bus.emit(
            EventData(EventTypeEnum.SYSTEM, SystemEventEnum.MAIN_TICK, {"dt": dt})
        )

        # FLUSH 3: Dispatch (User callbacks execute with fresh state)
        self.ctx.bus.process()

    def _process_buckets(self, dt: float):
        for name, bucket in self._buckets.items():
            bucket.accumulator += dt
            while bucket.accumulator >= bucket.interval:
                self.ctx.bus.emit(
                    EventData(
                        EventTypeEnum.SYSTEM,
                        SystemEventEnum.CUSTOM_TICK,
                        {"dt": bucket.interval, "label": name},
                    )
                )
                bucket.accumulator -= bucket.interval

    def _handle_exit(self, _):
        self.ctx.running = False

    def _shutdown(self):
        for manager in self.managers.values():
            manager.shutdown()


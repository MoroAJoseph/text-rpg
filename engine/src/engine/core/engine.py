from typing import Dict, Optional, Type
from .enums import EventTypeEnum, SystemEventEnum
from .dataclasses import EngineOptions, EventData, TickBucket
from .log import API_LOGGER
from .context import CTX
from .domain_manager import DomainManager, TDomainManager
from .clock import Clock
from .manager_registry import ManagerRegistry


class Engine:
    """The Root Kernel. Pure orchestrator for generic DomainManagers."""

    def __init__(self, options: EngineOptions = EngineOptions()):
        self.options = options
        self.ctx = CTX
        self.log = API_LOGGER
        self.managers = ManagerRegistry()
        self.clock = Clock(target_fps=60)

        self._buckets: Dict[str, TickBucket] = {
            name: TickBucket(name=name, target_rate=rate)
            for name, rate in self.options.rates.items()
        }

        self._bootstrap_domains()

        self.ctx.bus.subscribe(SystemEventEnum.ENGINE_STOP, self._handle_exit_signal)

    def _bootstrap_domains(self):
        """Resolves strings to classes and injects dependencies."""
        if self.options.input.enabled:
            # This import only happens here, preventing circularity
            from ..domains.input.registry import resolve_input_domain

            manager, driver = resolve_input_domain(self.options.input)
            manager.register_bus(self.ctx.bus)

            if driver:
                manager.register_driver(driver)

            self.register_manager("input", manager)

    def _emit_system_tick(self, name: SystemEventEnum, data: dict):
        self.ctx.bus.emit(EventData(type=EventTypeEnum.SYSTEM, name=name, data=data))

    def _handle_exit_signal(self, _):
        self.ctx.running = False

    def _on_shutdown(self):
        self.log.info("Engine Kernel: Initiating shutdown.")
        for manager in self.managers.values():
            try:
                manager.shutdown()
            except Exception as e:
                self.log.error(f"Kernel: Shutdown error: {e}")
        self.ctx.running = False

    def register_manager(self, name: str, manager: DomainManager):
        self.managers.add(name, manager)

    def run(self):
        self.ctx.running = True
        try:
            while self.ctx.running:
                self.update()
        except KeyboardInterrupt:
            pass
        finally:
            self._on_shutdown()

    def update(self):
        """
        The 3-Flush Cycle.
        Ensures input is polled, synced, and dispatched within one frame.
        """
        dt = self.clock.tick()

        # FLUSH 1: Cleanup old signals
        self.ctx.bus.process()

        # Step A: Domain Updates (Drivers poll hardware here)
        for manager in self.managers.values():
            manager.update(dt)

        # FLUSH 2: State Sync (Listeners now see new pressed/released states)
        self.ctx.bus.process()

        self._emit_system_tick(SystemEventEnum.ENGINE_TICK, {"dt": dt})

        # Step B: Fixed Multi-Rate Pulses (Physics/Network)
        for name, bucket in self._buckets.items():
            bucket.target_rate = self.options.rates.get(name, 0.0)
            if bucket.target_rate <= 0:
                continue

            bucket.accumulator += dt
            tick_count = 0

            while bucket.accumulator >= bucket.interval:
                # Safeguard against the "Spiral of Death"
                if tick_count >= self.options.max_ticks_per_frame:
                    bucket.accumulator = 0
                    break

                self._emit_system_tick(
                    SystemEventEnum.FIXED_TICK, {"dt": bucket.interval, "label": name}
                )
                bucket.accumulator -= bucket.interval
                tick_count += 1

        # FLUSH 3: Final Dispatch (Execute user callbacks)
        self.ctx.bus.process()

    def get_manager(
        self, name: str, expected_type: Type[TDomainManager]
    ) -> Optional[TDomainManager]:
        return self.managers.get(name, expected_type)

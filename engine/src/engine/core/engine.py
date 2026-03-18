from typing import Optional, Type

from .enums import EventTypeEnum, SystemEventEnum
from .dataclasses import EngineOptions, EventData, SystemEvent
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

        # Registry for pluggable domain components (Input, Renderer, etc.)
        self.managers = ManagerRegistry()

        # High-resolution clock for delta-time and frame-capping
        self.clock = Clock(target_fps=60)

        # Wire the global Event Bus to the Kernel's termination logic
        self.ctx.bus.subscribe(SystemEventEnum.ENGINE_STOP, self._handle_exit_signal)

    def register_manager(self, name: str, manager: DomainManager):
        """Standard way to plug in a Domain Manager."""
        self.managers.add(name, manager)

    def run(self):
        """The blocking entry point for the engine lifecycle."""
        self.log.info("Engine Kernel: Starting execution loop.")
        self.ctx.running = True

        try:
            while self.ctx.running:
                self.update()  # Now calls the helper method
        except KeyboardInterrupt:
            self.log.info("Engine Kernel: User interrupted via Keyboard.")
        finally:
            self._on_shutdown()

    def update(self):
        """
        Processes a single engine frame.
        Exposed for manual stepping in integration tests.
        """
        # Calculate delta time
        dt = self.clock.tick()

        # Process the BUS (Flush events from the PREVIOUS frame)
        self.ctx.bus.process()

        # Update Managers (They emit events for the NEXT frame)
        for manager in self.managers.values():
            manager.update(dt)

        # Emit TICK event
        tick_event = SystemEvent(
            type=EventTypeEnum.SYSTEM, name=SystemEventEnum.ENGINE_TICK, data={"dt": dt}
        )

        self.ctx.bus.emit(tick_event)

    def get_manager(
        self, name: str, expected_type: Type[TDomainManager]
    ) -> Optional[TDomainManager]:
        """
        Retrieves a manager from the registry and verifies its type.
        Used primarily by the API Factory to connect handles.
        """
        return self.managers.get(name, expected_type)

    def _handle_exit_signal(self, event):
        """Subscriber callback for SystemEventEnum.ENGINE_STOP."""
        self.log.info("Kernel: Termination signal received via Event Bus.")
        self.ctx.running = False

    def _on_shutdown(self):
        """Cleanup sequence ensuring all hardware drivers release resources."""
        self.log.info("Engine Kernel: Initiating shutdown sequence.")

        for manager in self.managers.values():
            try:
                manager.shutdown()
            except Exception as e:
                self.log.error(f"Kernel: Error shutting down manager: {e}")

        self.ctx.running = False
        self.log.info("Engine Kernel: Shutdown complete.")

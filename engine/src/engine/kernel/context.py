from ..core.bus import EventBus
from ..core.logger import Logger


class Context:
    """Shared kernel state and messaging hub."""

    def __init__(self):
        # Initialized with defaults, configured later by EngineFactory
        self.log_manager = Logger("engine_logs")
        self.log = self.log_manager.get_logger("KERNEL")
        self.bus: EventBus = EventBus()

        # State
        self.running: bool = False
        self.exit_code: int = 0


CTX = Context()

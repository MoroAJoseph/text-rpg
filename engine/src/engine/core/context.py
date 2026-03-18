from .event.engine_bus import EngineEventBus
from .log import LogManager


class Context:
    """Shared substrate state."""

    def __init__(self):
        self.log_manager = LogManager("engine_logs")
        self.system_log = self.log_manager.get_logger("ENGINE")
        self.bus: EngineEventBus = EngineEventBus()

        # State
        self.running: bool = False
        self.exit_code: int = 0


CTX = Context()

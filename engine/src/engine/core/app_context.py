from engine.managers.log import LogManager

from .event_bus import EngineEventBus


class AppContext:
    """The central registry for all active engine services."""

    def __init__(self):
        self.log_manager = LogManager("engine_logs")
        self.system_log = self.log_manager.get_logger("ENGINE")
        self.bus: EngineEventBus = EngineEventBus()
        self.renderer = None  # To be set by Driver
        self.input = None  # To be set by Driver
        self.telemetry = None
        self.running: bool = True
        self.exit_code: int = 0


# Create a single global instance for the Engine to use
CTX = AppContext()

from ..common.dataclasses import EngineOptions
from ..managers.log import API_LOGGER
from .app_context import CTX


class Engine:
    """The Root Kernel. Handles the loop and internal state."""

    def __init__(self, options: EngineOptions = EngineOptions()):
        self.options = options
        self.ctx = CTX
        self.log = API_LOGGER
        self.log.info(f"Engine Kernel Initialized: {options.width}x{options.height}")

    def run(self):
        """The actual blocking main loop."""
        self.ctx.running = True
        while self.ctx.running:
            self.ctx.bus.process()


def create_engine(options: EngineOptions = EngineOptions()) -> Engine:
    """Factory to produce a fresh Engine instance."""
    return Engine(options)

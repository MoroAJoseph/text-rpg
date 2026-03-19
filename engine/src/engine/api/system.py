from typing import TYPE_CHECKING
from ..core import EventTypeEnum, SystemEventEnum, EventData

if TYPE_CHECKING:
    from ..kernel import Engine


class SystemAPI:
    """Lifecycle control and logging."""

    def __init__(self, engine: "Engine"):
        self._bus = engine.ctx.bus
        self._log = engine.ctx.log

    def stop(self):
        """Request engine shutdown."""
        self._bus.emit(EventData(type=EventTypeEnum.SYSTEM, name=SystemEventEnum.STOP))

    def log(self, message: str, level: str = "info"):
        """Proxy to kernel logger."""
        method = getattr(self._log, level.lower(), self._log.info)
        method(message)

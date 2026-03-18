from typing import TYPE_CHECKING
from ..common.enums import EventTypeEnum, SystemEventEnum
from ..common.dataclasses import EventData

if TYPE_CHECKING:
    from ..core.kernel import Engine


class SystemAPI:
    """Controls engine lifecycle via intent-based events."""

    def __init__(self, engine: "Engine"):
        self._bus = engine.ctx.bus
        self.log = engine.log

    def start(self):
        self.log.info("API: System Start requested.")
        self._bus.emit(
            EventData(type=EventTypeEnum.SYSTEM, name=SystemEventEnum.ENGINE_START)
        )

    def shutdown(self):
        self.log.info("API: System Shutdown requested.")
        self._bus.emit(
            EventData(type=EventTypeEnum.SYSTEM, name=SystemEventEnum.ENGINE_STOP)
        )

    def tick(self):
        self._bus.emit(
            EventData(type=EventTypeEnum.SYSTEM, name=SystemEventEnum.ENGINE_TICK)
        )

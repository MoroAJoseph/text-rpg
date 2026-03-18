from typing import Protocol, TypeVar, runtime_checkable

from .event import EngineEventBus


@runtime_checkable
class DomainManager(Protocol):
    """The interface all domain managers must implement."""

    def register_bus(self, bus: EngineEventBus) -> None: ...
    def update(self, dt: float) -> None: ...
    def shutdown(self) -> None: ...


TDomainManager = TypeVar("TDomainManager", bound=DomainManager)

from typing import Protocol, Any, TypeVar, runtime_checkable
from engine.core.bus import EventBus


@runtime_checkable
class DomainDriver(Protocol):
    """The hardware interface contract."""

    def poll(self) -> Any:
        """Fetch raw hardware state."""
        ...

    def shutdown(self) -> None:
        """Release hardware locks (e.g., exit raw mode)."""
        ...


TDomainDriver = TypeVar("TDomainDriver", bound=DomainDriver)


@runtime_checkable
class DomainManager(Protocol):
    """The interface all domain managers must implement."""

    def register_bus(self, bus: EventBus) -> None: ...
    def update(self, dt: float) -> None: ...
    def shutdown(self) -> None: ...


TDomainManager = TypeVar("TDomainManager", bound=DomainManager)

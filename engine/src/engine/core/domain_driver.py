from typing import Protocol, Dict, Any, TypeVar, runtime_checkable


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

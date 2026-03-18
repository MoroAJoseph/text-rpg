from typing import Protocol, TypeVar, runtime_checkable


@runtime_checkable
class DomainManager(Protocol):
    """The interface all domain managers must implement."""

    def update(self, dt: float) -> None:
        """Called every frame. dt is the time in seconds since the last frame."""
        ...

    def shutdown(self) -> None:
        """Cleanup resources."""
        ...


TDomainManager = TypeVar("TDomainManager", bound=DomainManager)

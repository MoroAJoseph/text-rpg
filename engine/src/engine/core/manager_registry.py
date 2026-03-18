from typing import Dict, Optional, Type, ValuesView
from .domain_manager import DomainManager, TDomainManager


class ManagerRegistry:
    """A dedicated container for lifecycle-managed domain components."""

    def __init__(self):
        self._managers: Dict[str, DomainManager] = {}

    def __contains__(self, key: str) -> bool:
        return key in self._managers

    def add(self, name: str, manager: DomainManager):
        """Register a manager by a unique string key."""
        self._managers[name] = manager

    def get(
        self, name: str, expected_type: Type[TDomainManager]
    ) -> Optional[TDomainManager]:
        """Retrieve a manager and verify its type for the API."""
        manager = self._managers.get(name)
        if isinstance(manager, expected_type):
            return manager
        return None

    def values(self) -> ValuesView[DomainManager]:
        """
        Provides a view of all registered managers.
        Allows the Engine to iterate: for m in registry.values()
        """
        return self._managers.values()

    def all(self) -> Dict[str, DomainManager]:
        """Return the underlying dictionary of managers."""
        return self._managers

    def clear(self):
        """Flush the registry."""
        self._managers.clear()

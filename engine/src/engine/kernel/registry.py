from typing import Dict, Optional, Type, ValuesView
from ..core.domain_protocols import DomainManager, TDomainManager


class ManagerRegistry:
    """Container for managed domain components (Input, Display, etc)."""

    def __init__(self):
        self._managers: Dict[str, DomainManager] = {}

    def add(self, name: str, manager: DomainManager):
        self._managers[name] = manager

    def get(
        self, name: str, expected_type: Type[TDomainManager]
    ) -> Optional[TDomainManager]:
        manager = self._managers.get(name)
        return manager if isinstance(manager, expected_type) else None

    def values(self) -> ValuesView[DomainManager]:
        return self._managers.values()

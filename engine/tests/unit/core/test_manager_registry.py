import pytest
from unittest.mock import MagicMock
from engine.core import ManagerRegistry, DomainManager


class MockManager(DomainManager):
    def update(self, dt: float):
        pass

    def shutdown(self):
        pass


class OtherManager(DomainManager):
    def update(self, dt: float):
        pass

    def shutdown(self):
        pass


def test_registry_add_and_get():
    registry = ManagerRegistry()
    mock = MockManager()

    registry.add("test", mock)

    # Correct type retrieval
    assert registry.get("test", MockManager) == mock
    # Wrong type retrieval should return None
    assert registry.get("test", OtherManager) is None


def test_registry_values_view():
    registry = ManagerRegistry()
    m1, m2 = MockManager(), MockManager()

    registry.add("m1", m1)
    registry.add("m2", m2)

    managers = list(registry.values())
    assert len(managers) == 2
    assert m1 in managers
    assert m2 in managers


def test_registry_clear():
    registry = ManagerRegistry()
    registry.add("m1", MockManager())
    registry.clear()
    assert len(registry.all()) == 0

from engine.core.domain_protocols import DomainManager
from engine.kernel.registry import ManagerRegistry


class MockManager(DomainManager):
    def register_bus(self, bus):
        pass

    def update(self, dt):
        pass

    def shutdown(self):
        pass


class OtherManager(DomainManager):
    def register_bus(self, bus):
        pass

    def update(self, dt):
        pass

    def shutdown(self):
        pass


def test_registry_add_and_get():
    registry = ManagerRegistry()
    m = MockManager()
    registry.add("input", m)

    assert registry.get("input", MockManager) == m
    assert registry.get("input", OtherManager) is None


def test_registry_values_view():
    registry = ManagerRegistry()
    registry.add("a", MockManager())
    registry.add("b", MockManager())
    assert len(list(registry.values())) == 2

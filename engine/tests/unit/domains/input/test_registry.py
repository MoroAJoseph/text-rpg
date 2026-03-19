from engine.core.bus import EventBus
from engine.core.domain_protocols import DomainManager
from engine.kernel.registry import ManagerRegistry


class MockManager(DomainManager):

    def register_bus(self, bus: EventBus): ...
    def update(self, dt: float): ...
    def shutdown(self): ...


class OtherMockManager(DomainManager):
    """A separate valid manager for type-mismatch testing."""

    def register_bus(self, bus: EventBus): ...
    def update(self, dt: float): ...
    def shutdown(self): ...


def test_registry_add_and_get():
    registry = ManagerRegistry()
    mock = MockManager()
    registry.add("input", mock)

    # Success: types match perfectly
    assert registry.get("input", MockManager) == mock

    # Success: OtherMockManager is a valid DomainManager,
    # but it's not the type of the object stored at "input".
    # This proves the registry's type-safe filtering works.
    assert registry.get("input", OtherMockManager) is None

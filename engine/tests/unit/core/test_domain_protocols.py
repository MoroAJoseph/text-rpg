from engine.core.domain_protocols import DomainDriver, DomainManager


class ValidManager:
    def register_bus(self, bus):
        pass

    def update(self, dt):
        pass

    def shutdown(self):
        pass


class InvalidManager:
    def update(self, dt):
        pass


class ValidDriver:
    def poll(self):
        return []

    def shutdown(self):
        pass


def test_manager_protocol_compliance():
    # Verify Manager contract
    assert isinstance(ValidManager(), DomainManager)
    assert not isinstance(InvalidManager(), DomainManager)


def test_driver_protocol_compliance():
    # Verify Driver contract (Resolves Pylance "not accessed" warning)
    assert isinstance(ValidDriver(), DomainDriver)

    # A manager is not a driver
    assert not isinstance(ValidManager(), DomainDriver)

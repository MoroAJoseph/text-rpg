from engine import create_engine
from engine.core import DomainManager


class CleanupManager(DomainManager):
    def __init__(self):
        self.cleaned_up = False

    def update(self, dt: float):
        pass

    def shutdown(self):
        self.cleaned_up = True


def test_engine_cleans_up_all_managers():
    engine = create_engine()
    mock_manager = CleanupManager()

    # 1. Register a custom manager
    engine.register_manager("cleanup_test", mock_manager)

    # 2. Force a shutdown sequence
    engine._on_shutdown()

    # 3. Verify the manager's internal cleanup was called
    assert mock_manager.cleaned_up is True

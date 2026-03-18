import pytest
from engine import create_engine, EngineOptions


@pytest.fixture
def engine():
    """Returns a fresh engine instance for isolated testing."""
    return create_engine(EngineOptions())

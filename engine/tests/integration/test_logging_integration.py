from engine import create_engine


def test_engine_has_valid_logger():
    """Ensure every engine instance provides a functional logger."""
    engine = create_engine()
    assert engine.log is not None
    # Verify no exceptions on call
    engine.log.info("Instance-specific logging test")

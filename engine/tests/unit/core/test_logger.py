from engine.core.logger import Logger


def test_logger_creates_directory(tmp_path):
    log_dir = tmp_path / "logs"
    _ = Logger(log_dir=str(log_dir))
    assert log_dir.exists()


def test_fallback_logger_config(tmp_path):
    log_dir = tmp_path / "logs"
    l_manager = Logger(log_dir=str(log_dir))

    logger = l_manager.get_logger("UNIT_TEST")
    logger.info("Testing fallback")

    # Check if file was actually created
    log_file = log_dir / "engine.log"
    assert log_file.exists()

    with open(log_file, "r") as f:
        content = f.read()
        assert "UNIT_TEST" in content
        assert "INFO" in content

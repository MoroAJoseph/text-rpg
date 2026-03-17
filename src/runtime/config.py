from pathlib import Path
import yaml


class ConfigData:
    """
    Singleton-like runtime configuration / game state.
    Only one instance exists.
    """

    CONFIG_FILE: Path = Path("config/config.yaml")

    # Default values
    last_login: str = ""
    last_save_file: str = ""
    save_files: list[str] = []
    save_files_dir: str = "data/saves"

    def load(self) -> None:
        """Load configuration from YAML file."""
        if self.CONFIG_FILE.exists():
            with open(self.CONFIG_FILE, "r") as f:
                data = yaml.safe_load(f) or {}
            self.last_login = data.get("last_login", "")
            self.last_save_file = data.get("last_save_file", "")
            self.save_files = data.get("save_files", [])
            self.save_files_dir = data.get("save_files_dir", "data/saves")

    def save(self) -> None:
        """Save current configuration to YAML file."""
        self.CONFIG_FILE.parent.mkdir(exist_ok=True, parents=True)
        data = {
            "last_login": self.last_login,
            "last_save_file": self.last_save_file,
            "save_files": self.save_files,
            "save_files_dir": self.save_files_dir,
        }
        with open(self.CONFIG_FILE, "w") as f:
            yaml.safe_dump(data, f)


CONFIG_DATA = ConfigData()

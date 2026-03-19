import json
import pathlib
import tomllib
from typing import Any, Dict, Optional, Type, TypeVar

from .models import (
    CapabilityConfig,
    ControllerParameters,
    EngineConfig,
    InputCapabilities,
    InputConfig,
    KeyboardParameters,
    MouseParameters,
    TCapabilityParameters,
)


class ConfigLoader:
    """Orchestrates multi-format discovery and schema-validated loading."""

    DEFAULT_STEM = "config"
    SUPPORTED_EXTENSIONS = [".toml", ".json"]

    @staticmethod
    def discover_and_load(manual_path: Optional[str] = None) -> EngineConfig:
        """
        Priority:
        1. Manual Path (if provided)
        2. config.toml
        3. config.json
        """
        if manual_path:
            return ConfigLoader.load_file(manual_path)

        # Automatic Discovery
        for ext in ConfigLoader.SUPPORTED_EXTENSIONS:
            path = pathlib.Path(f"{ConfigLoader.DEFAULT_STEM}{ext}")
            if path.exists():
                return ConfigLoader.load_file(str(path))

        raise FileNotFoundError(
            "No configuration found. Provide a path or create config.toml/json."
        )

    @staticmethod
    def load_file(path: str) -> EngineConfig:
        """Reads file based on extension and passes to dict parser."""
        p = pathlib.Path(path)
        with open(p, "rb") as f:
            if p.suffix == ".toml":
                data = tomllib.load(f)
            elif p.suffix == ".json":
                data = json.load(f)
            else:
                raise ValueError(f"Unsupported config format: {p.suffix}")

        return ConfigLoader.load_from_dict(data)

    @staticmethod
    def load_from_dict(data: Dict[str, Any]) -> EngineConfig:
        """Core transformation logic from raw dictionary to EngineConfig."""
        engine_data = data.get("engine", {})
        feature_data = data.get("features", {})
        input_data = feature_data.get("input", {})
        caps_raw = input_data.get("capabilities", {})

        def _parse_cap(
            name: str, param_cls: Type[TCapabilityParameters]
        ) -> Optional[CapabilityConfig[TCapabilityParameters]]:
            if name not in caps_raw:
                return None

            c = caps_raw[name]
            raw_params = c.get("parameters", {})
            params = param_cls(**raw_params) if raw_params else param_cls()

            return CapabilityConfig(
                parameters=params,
                driver=c.get("driver", "default"),
                enabled=c.get("enabled", True),
                poll_rate=c.get("poll_rate"),
                log_level=c.get("log_level", "WARNING"),
            )

        input_capabilities = InputCapabilities(
            keyboard=_parse_cap("keyboard", KeyboardParameters)
            or CapabilityConfig(parameters=KeyboardParameters(), driver="default"),
            mouse=_parse_cap("mouse", MouseParameters),
            controller=_parse_cap("controller", ControllerParameters),
        )

        return EngineConfig(
            tick_rate=engine_data.get("tick_rate", 60),
            log_level=engine_data.get("log_level", "INFO"),
            rates=engine_data.get("rates", {}),
            input=InputConfig(
                enabled=input_data.get("enabled", True),
                default_poll_rate=input_data.get("default_poll_rate", 60.0),
                decay_threshold=input_data.get("decay_threshold", 0.12),
                capabilities=input_capabilities,
            ),
        )

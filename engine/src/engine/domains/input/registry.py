from typing import Optional

from engine.config.models import InputConfig, CapabilityConfig
from .manager import InputManager
from .drivers.blessed import BlessedInputDriver
from .drivers.default import DefaultInputDriver


def resolve_input_domain(config: InputConfig) -> InputManager:
    manager = InputManager(config)
    # Access the nested capabilities object
    caps = config.capabilities

    def _add_capability(name: str, capability: Optional[CapabilityConfig]):
        if not capability or not capability.enabled:
            return

        driver = None
        # Use asdict() or access .parameters directly if drivers expect a dict
        # Since our drivers use **kwargs, cap.parameters (a dataclass) works if
        # the driver __init__ matches the dataclass fields.
        params = (
            capability.parameters.__dict__
            if hasattr(capability.parameters, "__dict__")
            else {}
        )

        if capability.driver == "blessed":
            driver = BlessedInputDriver(**params)
        elif capability.driver in ("default", None):
            driver = DefaultInputDriver(**params)

        poll_rate = (
            capability.poll_rate
            if capability.poll_rate is not None
            else config.default_poll_rate
        )

        if driver:
            manager.add_spoke(name=name, driver=driver, rate=poll_rate)

    # Initialize from the capabilities dataclass
    _add_capability("keyboard", caps.keyboard)
    _add_capability("mouse", caps.mouse)
    _add_capability("controller", caps.controller)

    return manager

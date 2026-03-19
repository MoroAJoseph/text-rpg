from dataclasses import dataclass, field
from typing import Dict, Generic, Literal, Optional, TypeVar

TCapabilityParameters = TypeVar("TCapabilityParameters")

# --- Driver Literals ---

SupportedKeyboardDriver = Literal["default", "blessed"]
SupportedMouseDriver = Literal["default", "blessed"]
SupportedControllerDriver = Literal["default", "pygame"]
MouseTrackingProtocol = Literal["sgr", "x11", "urxvt"]
LogLevelLiteral = Literal["TRACE", "DEBUG", "INFO", "WARNING", "ERROR"]

# --- Generic Base ---


@dataclass
class CapabilityConfig(Generic[TCapabilityParameters]):
    """Generic hardware capabilities with strictly typed parameters.

    Attributes:
        parameters (TCompatabilityParameters): The specific parameter dataclass for this capability.
        driver (str): The identifier for the hardware driver to instantiate.
        enabled (bool): Whether this specific hardware capability is active.
        poll_rate (Optional[float]): Specific Hz to poll this hardware; defaults to domain rate if None.
        log_level (str): The verbosity of the driver's internal logging.
    """

    parameters: TCapabilityParameters
    driver: str = "default"
    enabled: bool = True
    poll_rate: Optional[float] = None
    log_level: LogLevelLiteral = "WARNING"


# --- Parameters ---


@dataclass
class KeyboardParameters:
    """Specific settings for terminal/keyboard drivers.

    Attributes:
        raw_mode (bool): Whether to put the terminal into raw mode (capturing control sequences).
        intercept_signals (bool): If True, prevents Ctrl+C from killing the process immediately.
        encoding (str): The character encoding to use for interpreting byte streams.
    """

    raw_mode: bool = True
    intercept_signals: bool = True
    encoding: str = "utf-8"


@dataclass
class MouseParameters:
    """Specific settings for mouse tracking.

    Attributes:
        tracking (MouseTrackingProtocol): The ANSI protocol used for mouse event reporting.
        report_release (bool): Whether to generate events when a mouse button is released.
    """

    tracking: MouseTrackingProtocol = "sgr"
    report_release: bool = True


@dataclass
class ControllerParameters:
    """Specific settings for gamepads.

    Attributes:
        device_index (int): The OS index of the controller hardware.
        deadzone (float): The threshold (0.0 to 1.0) to ignore minor analog stick movements.
        rumble_enabled (bool): Whether to enable haptic feedback if supported by the driver.
    """

    device_index: int = 0
    deadzone: float = 0.1
    rumble_enabled: bool = False


# --- Input Grouping ---


@dataclass
class InputCapabilities:
    """Input hardware capabilities with explicit instance defaults.

    Attributes:
        keyboard (CapabilityConfig[KeyboardParameters]): Configuration for keyboard input.
        mouse (Optional[CapabilityConfig[MouseParameters]]): Configuration for mouse input.
        controller (Optional[CapabilityConfig[ControllerParameters]]): Configuration for gamepad input.
    """

    keyboard: CapabilityConfig[KeyboardParameters] = field(
        default_factory=lambda: CapabilityConfig(
            driver="default", parameters=KeyboardParameters()
        )
    )
    mouse: Optional[CapabilityConfig[MouseParameters]] = field(
        default_factory=lambda: CapabilityConfig(
            driver="blessed", parameters=MouseParameters()
        )
    )
    controller: Optional[CapabilityConfig[ControllerParameters]] = field(
        default_factory=lambda: CapabilityConfig(
            driver="pygame", parameters=ControllerParameters()
        )
    )


# --- Root Configs ---


@dataclass
class InputConfig:
    """Input domain configuration.

    Attributes:
        enabled (bool): Global toggle for the entire input domain.
        default_poll_rate (float): The fallback frequency (Hz) for drivers without a specific rate.
        decay_threshold (float): Seconds of inactivity before a 'HELD' key is considered 'RELEASED'.
        capabilities (InputCapabilities): The specific hardware capabilities being managed.
    """

    enabled: bool = True
    default_poll_rate: float = 60.0
    decay_threshold: float = 0.12
    capabilities: InputCapabilities = field(default_factory=InputCapabilities)


@dataclass
class EngineConfig:
    """The Master Manifest (The Scope).

    Attributes:
        tick_rate (int): The primary target frequency (Hz) for the main engine loop.
        log_level (str): The global logging verbosity for the engine kernel.
        rates (Dict[str, float]): A map of custom tick rates for specialized background buckets.
        input (InputConfig): The configuration scope for the Input Domain.
    """

    tick_rate: int = 60
    log_level: LogLevelLiteral = "INFO"
    rates: Dict[str, float] = field(default_factory=dict)
    input: InputConfig = field(default_factory=InputConfig)

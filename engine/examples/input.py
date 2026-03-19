import sys
import select
import os
import contextlib
from typing import cast  # Use typing, NOT ctypes
from blessed import Terminal
from engine import (
    create_engine,
    connect,
    EventTypeEnum,
    KeyInputEnum,
    InputEventNameEnum,
    SystemEventEnum,
)
from engine.domains.input.drivers.default import DefaultInputDriver
from engine.domains.input.manager import InputManager

term = Terminal()

config_data = {
    "engine": {"tick_rate": 60, "log_level": "INFO", "rates": {}},
    "features": {
        "input": {
            "enabled": True,
            "default_poll_rate": 60.0,
            "decay_threshold": 0.12,
            "capabilities": {
                "keyboard": {
                    "driver": "default",
                    "enabled": True,
                    "parameters": {"raw_mode": True},
                },
                "mouse": {
                    "driver": "default",
                    "enabled": True,
                    "parameters": {"tracking": "sgr"},
                },
            },
        }
    },
}

engine = create_engine(config_data)
api = connect(engine)
input_history = []

# --- Buffer Feeding Logic ---


def feed_input_driver(_):
    manager_instance = engine.managers.get("input", InputManager)
    manager = cast(InputManager, manager_instance)

    if not manager:
        return

    for spoke in manager._spokes:
        if isinstance(spoke.driver, DefaultInputDriver):
            # Check if file descriptor 0 (stdin) has data waiting
            if select.select([sys.stdin], [], [], 0)[0]:
                try:
                    # os.read(0, size) is non-blocking on most Unix-like systems
                    # when used after select. grab up to 4kb of sequences.
                    raw_bytes = os.read(sys.stdin.fileno(), 4096)
                    if raw_bytes:
                        # Decode and push the whole chunk to the driver buffer
                        chunk = raw_bytes.decode(errors="ignore")
                        spoke.driver._buffer.append(chunk)
                except OSError:
                    pass


# --- Diagnostic Rendering ---


def render_ui():
    print(term.home + term.clear)
    print(term.bold_white_on_blue(" --- ENGINE INPUT DIAGNOSTIC --- "))
    print(
        f"Stack Size: {len(input_history)}/15 | Tick Rate: {engine.clock.tick_rate:.1f}Hz"
    )
    print("-" * 60)

    if not input_history:
        print(term.italic("Waiting for hardware input... (Type or Click)"))
    else:
        for i, event in enumerate(reversed(input_history)):
            payload = event.data
            display_name = payload.identifier

            if payload.identifier == KeyInputEnum.CHAR:
                display_name = f"CHAR('{payload.raw_data}')"

            coord_info = f" @ {payload.coords}" if payload.coords != (0, 0) else ""
            print(
                f"[{i:02}] ID: {str(display_name):<22} | "
                f"STATE: {payload.state.name:<10} | "
                f"RAW: {repr(payload.raw_data)}{coord_info}"
            )


def on_input(event):
    if event.name == InputEventNameEnum.TELEMETRY:
        return
    input_history.append(event)
    if len(input_history) > 15:
        input_history.pop(0)
    render_ui()


# --- Subscriptions ---

api.events.on_type(EventTypeEnum.INPUT, on_input)
api.events.on(SystemEventEnum.MAIN_TICK, feed_input_driver)


@contextlib.contextmanager
def terminal_lifecycle(terminal):
    with terminal.fullscreen(), terminal.cbreak(), terminal.hidden_cursor():
        # Clear screen and enable mouse tracking
        print(terminal.home + terminal.clear + terminal.enter_mouse, end="", flush=True)
        yield
        print(terminal.exit_mouse, end="", flush=True)


if __name__ == "__main__":
    with terminal_lifecycle(term):
        render_ui()
        try:
            engine.run()
        except KeyboardInterrupt:
            pass

import signal
from runtime.singletons import (
    GAME_MANAGER,
    LOGGER,
)
from models.enums import ExitCodeEnum


def setup_signals():
    """
    Hooks OS signals to the specific GameManager instance.
    The signal module expects a function with (sig, frame) arguments.
    """

    exit_signals = {
        signal.SIGINT: (ExitCodeEnum.TERMINATED_BY_USER, "User pressed Ctrl+C"),
        signal.SIGTERM: (ExitCodeEnum.TERMINATED, "Process terminated by System"),
    }

    # Hang Up (terminal closed) (Unix-like systems
    if hasattr(signal, "SIGHUP"):
        exit_signals[signal.SIGHUP] = (ExitCodeEnum.TERMINATED, "Terminal hung up")

    def handle_signal(sig, frame):
        # Window Change (Resize)
        if hasattr(signal, "SIGWINCH") and sig == signal.SIGWINCH:
            from runtime.singletons import UI_MANAGER

            UI_MANAGER.render()
            return

        # Exit
        exit_data = exit_signals.get(sig)
        if exit_data:
            code, msg = exit_data
            LOGGER.info(f"OS signal [{sig}] intercepted: {msg}")
            GAME_MANAGER.request_exit(code, msg)

    def register_signals():
        # Exits
        for sig in exit_signals:
            signal.signal(sig, handle_signal)

        # Window Change
        if hasattr(signal, "SIGWINCH"):
            signal.signal(signal.SIGWINCH, handle_signal)

    register_signals()


if __name__ == "__main__":
    setup_signals()
    GAME_MANAGER.bootloader()
    GAME_MANAGER.main_loop()
    GAME_MANAGER.handle_exit()

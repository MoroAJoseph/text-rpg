import signal
from src.runtime.core.event_bus import EVENT_BUS
from src.runtime.core.logger import LOGGER
from src.runtime.managers.game import GAME_MANAGER
from src.runtime.managers.ui import UI_MANAGER
from src.models.type_models import Event, EventTypeEnum, ExitCodeEnum, GameEventsEnum


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
            UI_MANAGER.render()
            return

        # Exit
        exit_data = exit_signals.get(sig)
        if exit_data:
            code, msg = exit_data
            LOGGER.info(f"OS signal [{sig}] intercepted: {msg}")
            # Corrected to a dictionary
            EVENT_BUS.emit(
                Event(
                    EventTypeEnum.GAME,
                    GameEventsEnum.EXIT_GAME,
                    {"code": code, "msg": msg},
                )
            )

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

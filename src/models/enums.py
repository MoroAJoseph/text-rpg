from enum import Enum


class ExitCodeEnum(Enum):
    SUCCESS = 0  # The script executed without errors or issues. This is the default exit code if the script finishes normally without any uncaught exceptions or explicit sys.exit() call.
    GENERAL_ERROR = 1  # A general catch-all for an application error or failure. This is the default exit code if the interpreter exits due to an unhandled exception.
    CLI_ERROR = 2  # Misuse of shell built-ins or invalid command-line arguments. Python's argparse module commonly uses this for invalid arguments.
    CANNOT_EXECUTE = 126  # Permission problem or the command is not an executable.
    COMMAND_NOT_FOUND = 127  # The command line tool the script tried to run could not be found (e.g., an issue with the system's $PATH environment variable).
    TERMINATED_BY_USER = 130  # The script was interrupted and terminated by a SIGINT signal (typically from a user pressing Ctrl+C).
    TERMINATED = 143  # The process received a graceful termination signal (SIGTERM), often used by container orchestrators like Kubernetes.
    OUT_OF_RANGE = 255  # Used when the exit status provided was outside the acceptable range of 0-255.


class GameStateEnum(Enum):
    BOOT = 1
    MAIN = 2
    EXIT = 3


class UIScreensEnum(Enum):
    MAIN_MENU = 1
    BLACKSMITH_SHOP_MENU = 2
    WEAPON_UPGRADE_MENU = 2


class GearSlotEnum(Enum):
    WEAPON = 1
    HEAD = 2
    CHEST = 3
    RING = 4
    NECK = 5

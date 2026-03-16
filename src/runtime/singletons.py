from logging import Logger

from runtime.logger import setup_logger
from runtime.managers.game import GameManager
from runtime.managers.ui import UIManager
from ui.screens.main import MainGameScreen
from ui.screens.title import TitleScreen

# Telemetry
LOGGER: Logger = setup_logger("Dev")

# Managers
UI_MANAGER = UIManager(logger=LOGGER)
GAME_MANAGER = GameManager(logger=LOGGER, ui_manager=UI_MANAGER)

# Screens
TITLE_SCREEN = TitleScreen()
MAIN_GAME_SCREEN = MainGameScreen()

from ui.components.overlay import UIOverlay
from models.enums import ExitCodeEnum


class MainMenu(UIOverlay):
    def __init__(self):
        self.options = ["New Game", "Load Game", "Exit"]
        self.index = 0

    def draw(self, buffer):
        w, h = 30, 8
        x, y = (buffer.width - w) // 2, (buffer.height - h) // 2
        self.draw_box(buffer, x, y, w, h, "Main Menu")

        for i, opt in enumerate(self.options):
            # The "Carrot" logic: prefix changes based on self.index
            prefix = " > " if i == self.index else "   "
            buffer.write(x + 4, y + 3 + i, f"{prefix}{opt}")

    def handle_input(self, user_input: str) -> None:
        from runtime.singletons import UI_MANAGER, GAME_MANAGER
        from ui.screens.main import MainGameScreen
        from ui.menus.welcome import WelcomeMenu

        # InputManager now sends "up", "down", "enter"
        if user_input == "up":
            self.index = (self.index - 1) % len(self.options)
        elif user_input == "down":
            self.index = (self.index + 1) % len(self.options)
        elif user_input == "enter":
            self.execute_selection()

    def execute_selection(self):
        from runtime.singletons import UI_MANAGER, GAME_MANAGER
        from ui.screens.main import MainGameScreen
        from ui.menus.welcome import WelcomeMenu

        choice = self.options[self.index]
        if choice == "New Game":
            UI_MANAGER.set_screen(MainGameScreen())
            UI_MANAGER.pop_overlay()
            UI_MANAGER.push_overlay(WelcomeMenu())
        elif choice == "Exit":
            GAME_MANAGER.request_exit(ExitCodeEnum.SUCCESS, "User quit")

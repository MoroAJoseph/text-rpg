from ui.components.overlay import UIOverlay


class WelcomeMenu(UIOverlay):
    def draw(self, buffer):
        w, h = 40, 5
        x, y = (buffer.width - w) // 2, (buffer.height - h) // 2
        self.draw_box(buffer, x, y, w, h, "WELCOME")
        buffer.write(x + 4, y + 2, "Welcome to the Sandbox, Hero!")

    def handle_input(self, user_input):
        from runtime.singletons import UI_MANAGER

        # Use the specific overlay method we defined in UIManager
        if user_input == "":
            UI_MANAGER.pop_overlay()

import sys
import tty
import termios


class InputManager:
    @staticmethod
    def get_key() -> str:
        """Reads a single keypress from stdin in raw mode."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        ch = ""
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            # Handle escape sequences (Arrows)
            if ch == "\x1b":
                # Only read more if there's data to avoid hanging
                ch += sys.stdin.read(2)
        except Exception:
            ch = ""
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    @staticmethod
    def map_key(ch: str) -> str:
        """Maps raw characters to standard internal strings."""
        if not ch:
            return ""

        mappings = {
            "\x1b[A": "up",
            "\x1b[B": "down",
            "\x1b[C": "right",
            "\x1b[D": "left",
            "\r": "enter",
            "\x7f": "backspace",
        }
        # Explicitly return a string to satisfy Pylance
        return str(mappings.get(ch, ch))

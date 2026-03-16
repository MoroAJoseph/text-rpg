import sys


class UIBuffer:
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.grid = [[" " for _ in range(width)] for _ in range(height)]

    def write(self, x: int, y: int, text: str, transparent: bool = False):
        for i, char in enumerate(text):
            tx = x + i
            if 0 <= tx < self.width and 0 <= y < self.height:
                if transparent and char == " ":
                    continue
                self.grid[y][tx] = char

    def render_to_terminal(self):
        """Renders the grid using absolute positioning to prevent scrolling."""
        output = []
        for y, row in enumerate(self.grid):
            # \033[{y+1};1H moves cursor to row y+1, column 1
            # \033[K clears from cursor to end of line
            line = f"\033[{y+1};1H" + "".join(row) + "\033[K"
            output.append(line)

        sys.stdout.write("".join(output))

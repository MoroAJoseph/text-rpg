class HealthComponent:

    def __init__(self, current: int, maximum: int):
        self.current: int = current
        self.maximum: int = maximum

    def change_current(self, value: int):
        self.current = max(0, self.current + value)

    def change_max(self, value: int):
        self.maximum = max(0, self.maximum + value)

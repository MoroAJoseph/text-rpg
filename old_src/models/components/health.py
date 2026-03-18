from ..type_models import HealthComponentData


class HealthComponent:

    def __init__(self, data: HealthComponentData):
        self.current: float = data.CurrentHealth
        self.maximum: int = data.MaxHealth

    def change_current(self, value: float):
        self.current = max(0, self.current + value)

    def change_max(self, value: int):
        self.maximum = max(0, self.maximum + value)

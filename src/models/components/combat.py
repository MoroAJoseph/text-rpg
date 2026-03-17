from ..type_models import CombatComponentData


class CombatComponent:

    def __init__(self, data: CombatComponentData):
        self.can_attack: bool = data.CanAttack
        self.can_defend: bool = data.CanDefend

    def change_can_attack(self, value: bool):
        self.can_attack = value

    def change_can_defend(self, value: bool):
        self.can_defend = value

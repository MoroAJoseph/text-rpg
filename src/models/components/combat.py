class CombatComponent:

    def __init__(self, can_attack: bool, can_defend: bool):
        self.can_attack: bool = can_attack
        self.can_defend: bool = can_defend

    def change_can_attack(self, value: bool):
        self.can_attack = value

    def change_can_defend(self, value: bool):
        self.can_defend = value

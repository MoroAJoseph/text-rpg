from models.characters.character import Character
from models.components.health import HealthComponent
from models.components.combat import CombatComponent


class Enemy(Character):

    def __init__(
        self,
        name: str,
        health_component: HealthComponent,
        combat_component: CombatComponent,
    ):
        super().__init__(name)
        self.health_component = health_component
        self.combat_component = combat_component

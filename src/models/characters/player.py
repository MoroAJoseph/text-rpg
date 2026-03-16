from models.characters.character import Character
from models.components.health import HealthComponent
from models.components.combat import CombatComponent
from models.components.inventory import InventoryComponent


class Player(Character):

    def __init__(self, name: str, initial_current_health: int, initial_max_health: int):
        super().__init__(name)
        self.health_component = HealthComponent(
            current=initial_current_health, maximum=initial_max_health
        )
        self.combat_component = CombatComponent(can_attack=True, can_defend=True)
        self.inventory_component = InventoryComponent(slots=20, item_stacks=[])

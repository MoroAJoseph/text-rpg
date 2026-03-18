from ..components.health import HealthComponent
from ..components.combat import CombatComponent
from ..components.inventory import InventoryComponent
from ..type_models import CharacterEntityData, PlayerEntityData
from .character import Character


class Player(Character):

    def __init__(self, data: PlayerEntityData):
        character_data = CharacterEntityData(data.Name)
        super().__init__(data=character_data)
        self.health_component = HealthComponent(data=PlayerEntityData.HealthComponent)
        self.combat_component = CombatComponent(data=PlayerEntityData.CombatComponent)
        self.inventory_component = InventoryComponent(
            data=PlayerEntityData.InventoryComponent
        )

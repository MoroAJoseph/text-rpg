from ..components.health import HealthComponent
from ..components.combat import CombatComponent
from ..type_models import CharacterEntityData, EnemyEntityData
from .character import Character


class Enemy(Character):

    def __init__(self, data: EnemyEntityData):
        character_data = CharacterEntityData(data.Name)
        super().__init__(data=character_data)
        self.health_component = HealthComponent(data=EnemyEntityData.HealthComponent)
        self.combat_component = CombatComponent(data=EnemyEntityData.CombatComponent)

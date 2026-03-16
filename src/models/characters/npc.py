from typing import List

from models.characters.character import Character
from models.components.inventory import InventoryComponent, ItemStack


class Merchant(Character):

    def __init__(
        self, name: str, inventory_slots: int, inventory_item_stacks: List[ItemStack]
    ):
        super().__init__(name)
        self.inventory_component = InventoryComponent(
            slots=inventory_slots, item_stacks=inventory_item_stacks
        )


class Blacksmith(Character):

    def __init__(
        self, name: str, inventory_slots: int, inventory_item_stacks: List[ItemStack]
    ):
        super().__init__(name)
        self.inventory_component = InventoryComponent(
            slots=inventory_slots, item_stacks=inventory_item_stacks
        )

from models.type_models import GearSlotEnum
from models.items.item import Item


class Gear(Item):

    def __init__(
        self,
        name: str,
        description: str,
        max_in_inventory: int,
        value: int,
        slot: GearSlotEnum,
    ):
        max_stack = 1
        super().__init__(name, description, max_stack, max_in_inventory, value)
        self.slot: GearSlotEnum = slot

from ..type_models import GearComponentData, GearSlotEnum
from ..items.gear import Gear


class GearSlot:

    def __init__(self, slot_type: GearSlotEnum, gear: Gear | None = None):
        self.type: GearSlotEnum = slot_type
        self.gear: Gear | None = gear


class GearComponent:

    def __init__(self, data: GearComponentData):
        self.weapon_slot = GearSlot(GearSlotEnum.WEAPON, data.Weapon)
        self.head_slot = GearSlot(GearSlotEnum.HEAD, data.Head)
        self.chest_slot = GearSlot(GearSlotEnum.CHEST, data.Chest)
        self.ring_slot = GearSlot(GearSlotEnum.RING, data.Ring)
        self.neck_slot = GearSlot(GearSlotEnum.NECK, data.Neck)

    def get_slot_by_type(self, slot_type: GearSlotEnum) -> GearSlot:
        match slot_type:
            case GearSlotEnum.WEAPON:
                return self.weapon_slot
            case GearSlotEnum.HEAD:
                return self.head_slot
            case GearSlotEnum.CHEST:
                return self.chest_slot
            case GearSlotEnum.RING:
                return self.ring_slot
            case GearSlotEnum.NECK:
                return self.neck_slot

    def equip(self, gear: Gear, slot_type: GearSlotEnum) -> Gear | None:
        # Gear must match slot
        if gear.slot != slot_type:
            print(f"Cannot equip {gear.name} into {slot_type}")
            return None

        target_slot: GearSlot = self.get_slot_by_type(slot_type)
        old_gear: Gear | None = target_slot.gear

        # Perform the swap
        target_slot.gear = gear
        return old_gear

    def unequip(self, slot_type: GearSlotEnum) -> Gear | None:
        target_slot: GearSlot = self.get_slot_by_type(slot_type)

        if target_slot.gear is None:
            print(f"Slot {slot_type} is already empty.")
            return None

        removed_gear: Gear = target_slot.gear
        target_slot.gear = None

        return removed_gear

from typing import List

from ..items.item import Item
from ..type_models import InventoryComponentData


class ItemStack:

    def __init__(self, item: Item, count: int):
        self.item: Item = item
        self.count: int = count

    @property
    def is_full(self):
        return self.item.max_stack == self.count

    def change_count(self, value: int):
        self.count = max(0, self.count + value)


class InventoryComponent:

    def __init__(self, data: InventoryComponentData):
        self.slots: int = data.InventorySlots
        self.item_stacks: List[ItemStack] = data.InventoryItems

    @property
    def used_slots(self):
        return len(self.item_stacks)

    def get_total_item_count(self, item_name: str) -> int:
        return sum(
            stack.count for stack in self.item_stacks if stack.item.name == item_name
        )

    def change_slots(self, value: int):
        self.slots = max(0, self.slots + value)

    def add_item(
        self, item: Item, count: int, stop_after_stack_filled: bool = False
    ) -> int:
        # Reject non-positive requests immediately
        if count <= 0:
            return 0

        # Calculate global cap allowance to ensure sandbox limits are respected
        current_total = self.get_total_item_count(item.name)
        allowed_by_cap = max(0, item.max_in_inventory - current_total)

        # We only process what the global cap allows
        to_process = min(count, allowed_by_cap)

        # If the inventory already has the maximum allowed for this item, return zero
        if to_process <= 0:
            return 0

        # Store the initial allowed amount to calculate the final added total
        initial_allowed = to_process

        # Identify existing stacks of the same item that have room for more
        partial_stacks = [
            s for s in self.item_stacks if s.item.name == item.name and not s.is_full
        ]

        # Fill existing partial stacks before using new slots
        for stack in partial_stacks:
            space_in_stack = stack.item.max_stack - stack.count
            transfer = min(to_process, space_in_stack)

            stack.change_count(transfer)
            to_process -= transfer

            # Exit if we have no more items or if the flag restricts us to one stack
            if to_process == 0 or stop_after_stack_filled:
                return initial_allowed - to_process

        # Utilize empty slots if there is still an amount remaining to add
        # This loop runs multiple times if the remaining count exceeds one max_stack
        while to_process > 0 and len(self.item_stacks) < self.slots:
            transfer = min(to_process, item.max_stack)

            new_stack = ItemStack(item, transfer)
            self.item_stacks.append(new_stack)
            to_process -= transfer

            # If flag is active, we stop after creating exactly one new stack
            if stop_after_stack_filled:
                break

        # Return the total successfully committed to the inventory
        return initial_allowed - to_process

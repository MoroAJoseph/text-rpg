class Item:

    def __init__(
        self,
        name: str,
        description: str,
        max_stack: int,
        max_in_inventory: int,
        value: int,
    ):
        self.name: str = name
        self.description: str = description
        self.max_stack: int = max_stack
        self.max_in_inventory: int = max_in_inventory
        self.value: int = value

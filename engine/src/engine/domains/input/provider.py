from typing import List, Protocol

from .dataclasses import InputEvent


class InputProvider(Protocol):
    """
    Interface for input drivers.
    A provider must return a list of InputEvents on every poll.
    """

    def poll(self) -> List[InputEvent]: ...

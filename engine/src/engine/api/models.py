from dataclasses import dataclass
from typing import Optional
from .events import EventsAPI
from .system import SystemAPI
from .input import InputAPI


@dataclass
class APIStack:
    """The unified interface for the developer."""

    events: EventsAPI
    system: SystemAPI
    input: Optional[InputAPI] = None

import time
from typing import List, Any

from engine.core.domain_protocols import DomainDriver
from ..models import InputPayload
from ..enums import InputStateEnum


class InputDriver(DomainDriver):
    """Substrate for all input hardware adapters."""

    def poll(self) -> List[InputPayload]:
        raise NotImplementedError("Poll must be implemented by specific driver.")

    def shutdown(self) -> None:
        """Default no-op shutdown for input drivers."""
        pass

    def _create_payload(
        self,
        identifier: Any,
        state: InputStateEnum,
        raw: Any,
        coords: tuple[int, int] = (0, 0),
    ) -> InputPayload:
        """Standardized payload factory for all drivers."""
        return InputPayload(
            identifier=identifier,
            state=state,
            timestamp=time.perf_counter(),
            coords=coords,
            raw_data=str(raw),
        )

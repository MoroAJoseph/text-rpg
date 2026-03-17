from typing import List, Callable
from models.type_models import UIScreensEnum  # Assuming you'll map screens to enums


class InteractionRequirement:
    def __init__(
        self, description: str, check_func: Callable[[], bool], fail_message: str
    ):
        self.description: str = description
        self.check_func: Callable[[], bool] = check_func
        self.fail_message: str = fail_message


class InteractionComponent:

    def __init__(
        self,
        screen_type: UIScreensEnum,
        requirements: List[InteractionRequirement] | None = None,
    ):
        self.screen_type = screen_type
        self.requirements = requirements or []

    @property
    def can_interact(self) -> bool:
        """Returns True if all requirements are met."""
        return all(requirement.check_func() for requirement in self.requirements)

    def get_failed_requirements(self) -> List[InteractionRequirement]:
        """Returns the list of requirements currently not met."""
        return [
            requirement
            for requirement in self.requirements
            if not requirement.check_func()
        ]

from .manager import InputManager
from .drivers.blessed import BlessedInputDriver


def resolve_input_domain(opts):
    # Manager instantiation is now clean
    manager = InputManager()

    driver = None
    if opts.driver == "blessed":
        driver = BlessedInputDriver(**opts.driver_args)

    return manager, driver

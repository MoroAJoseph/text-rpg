import contextlib

from blessed import Terminal
from engine import (
    create_engine,
    connect,
    EventTypeEnum,
    EngineOptions,
    InputOptions,
    SystemEventEnum,
    KeyInputEnum,
)

term = Terminal()
options = EngineOptions(input=InputOptions().use_terminal(term))
engine = create_engine(options)
api = connect(engine)

input_history = []


def render_diagnostic():
    # Use term.home to move cursor to (0,0) and term.clear to wipe the screen
    # Wrapping it in a single print call reduces flicker
    output = [
        term.home + term.clear,
        "--- ENGINE INPUT DIAGNOSTIC ---",
        f"Status: Polling @ {engine.clock.fps:.1f} FPS",  # Accesses the @property
        "Instructions: Press keys. Only one event per action.",
        "-" * 45,
    ]

    if not input_history:
        output.append("Waiting for input...")
    else:
        for i, event in enumerate(reversed(input_history)):
            display_name = event.name

            # Handle the CHAR metadata correctly
            if event.name == KeyInputEnum.CHAR:
                char_val = event.data.raw_data
                display_name = f"CHAR('{char_val}')"

            # Use fixed-width formatting for the ID to prevent layout shifting
            line = f"[{i}] ID: {str(display_name):<25} | STATE: {event.data.state.name}"
            output.append(line)

    # Join and print once to avoid terminal 'stutter'
    print("\n".join(output))


def on_input(event):
    input_history.append(event)
    if len(input_history) > 15:  # Keep a bit more history
        input_history.pop(0)


def on_engine_tick(_):
    render_diagnostic()


api.events.on_type(EventTypeEnum.INPUT, on_input)
api.events.on(SystemEventEnum.ENGINE_TICK, on_engine_tick)


@contextlib.contextmanager
def mouse_handler(terminal):
    print(terminal.enter_mouse, end="", flush=True)
    try:
        yield
    finally:
        print(terminal.exit_mouse, end="", flush=True)


# Usage in your script
with term.fullscreen(), term.cbreak(), term.hidden_cursor(), mouse_handler(term):
    engine.run()

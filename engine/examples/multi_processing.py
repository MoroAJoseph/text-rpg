from blessed import Terminal
from engine import (
    create_engine,
    connect,
    EngineOptions,
    InputOptions,
    SystemEventEnum,
    KeyInputEnum,
)

term = Terminal()
options = EngineOptions(
    rates={"red": 0.5, "blue": 2.0, "yellow": 1.0},
    input=InputOptions().use_terminal(term),
)

engine = create_engine(options)
api = connect(engine)

state = {
    "red_flash": False,
    "blue_flash": False,
    "yellow_flash": False,
    "green_acc": 0.0,
    "red_acc": 0.0,
    "blue_acc": 0.0,
    "yellow_acc": 0.0,
    "yellow_rate": 1.0,
}


def get_bar(current, total, width=30):
    fraction = min(current / total, 1.0) if total > 0 else 1.0
    filled = int(fraction * width)
    return f"[{'#' * filled}{'-' * (width - filled)}] {int(fraction * 100):>3}%"


def render():
    print(term.home + term.clear)
    # Status squares
    g_sq = "\033[92m■\033[0m"
    r_sq = "\033[91m■\033[0m" if state["red_flash"] else " "
    b_sq = "\033[94m■\033[0m" if state["blue_flash"] else " "
    y_sq = "\033[93m■\033[0m" if state["yellow_flash"] else " "

    print(f"TICKS: Green {g_sq} | Red {r_sq} | Blue {b_sq} | Yellow {y_sq}")
    print(f"CONTROLS: [UP/DOWN] to adjust Yellow Rate: {state['yellow_rate']:.2f} Hz")
    print("=" * 60)

    y_int = 1.0 / state["yellow_rate"] if state["yellow_rate"] > 0 else 1.0
    print(f"Green (Main/1s Loop): {get_bar(state['green_acc'], 1.0)}")
    print(f"Red   (Fixed/2.0s):   {get_bar(state['red_acc'], 2.0)}")
    print(f"Blue  (Fixed/0.5s):   {get_bar(state['blue_acc'], 0.5)}")
    print(f"Yellow(Dynamic):      {get_bar(state['yellow_acc'], y_int)}")

    # Reset flash markers
    state["red_flash"] = state["blue_flash"] = state["yellow_flash"] = False


def on_engine_tick(event):
    dt = event.data["dt"]

    # Input handling via the reflected API
    if api.input:
        if api.input.is_pressed(KeyInputEnum.UP):
            state["yellow_rate"] = min(state["yellow_rate"] + 0.1, 30.0)
        if api.input.is_pressed(KeyInputEnum.DOWN):
            state["yellow_rate"] = max(state["yellow_rate"] - 0.1, 0.1)

    # Sync rate back to the engine buckets
    engine.options.rates["yellow"] = state["yellow_rate"]

    state["green_acc"] = (state["green_acc"] + dt) % 1.0
    state["red_acc"] += dt
    state["blue_acc"] += dt
    state["yellow_acc"] += dt
    render()


def on_fixed_tick(event):
    label = event.data.get("label")
    flash_key = f"{label}_flash"
    acc_key = f"{label}_acc"

    if flash_key in state:
        state[flash_key] = True
        state[acc_key] = 0.0


api.events.on(SystemEventEnum.ENGINE_TICK, on_engine_tick)
api.events.on(SystemEventEnum.FIXED_TICK, on_fixed_tick)

with term.cbreak(), term.hidden_cursor():
    engine.run()

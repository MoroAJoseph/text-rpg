from enum import Enum
from engine import EventData, EventTypeEnum, KeyInputEnum
from engine.core import EngineEventBus, BaseEventBus


class AudioSubject(Enum):
    PLAY_SFX = "play_sfx"
    STOP_MUSIC = "stop_music"


# You must provide BOTH the Enum type and the Event Data type
class AudioBus(BaseEventBus[AudioSubject, EventData]):
    """A bus specialized for Audio subjects using standard EventData."""

    def _get_event_name(self, event: EventData) -> AudioSubject | None:
        # Cast or verify that the event name is indeed an AudioSubject
        if isinstance(event.name, AudioSubject):
            return event.name
        return None


def test_custom_bus_functional_isolation():
    audio_bus = AudioBus()
    triggered = []

    def on_play(event: EventData):
        triggered.append(event.data)

    # Subscribe to custom enum
    audio_bus.subscribe(AudioSubject.PLAY_SFX, on_play)

    # Emit custom data
    audio_bus.emit(
        EventData(
            type=EventTypeEnum.SYSTEM, name=AudioSubject.PLAY_SFX, data="explosion.wav"
        )
    )

    # Verification of inheritance logic
    assert len(audio_bus._next_queue) == 1
    audio_bus.process()
    assert "explosion.wav" in triggered


def test_event_bus_separation():
    bus = EngineEventBus()
    results = []

    def on_up(event: EventData):
        results.append("UP_PROCESSED")
        # Emit a new event during processing
        bus.emit(EventData(type=EventTypeEnum.INPUT, name=KeyInputEnum.DOWN))

    bus.subscribe(KeyInputEnum.UP, on_up)
    bus.subscribe(KeyInputEnum.DOWN, lambda e: results.append("DOWN_PROCESSED"))

    bus.emit(EventData(type=EventTypeEnum.INPUT, name=KeyInputEnum.UP))

    bus.process()
    assert "UP_PROCESSED" in results
    assert "DOWN_PROCESSED" not in results  # Should be in next queue

    bus.process()
    assert "DOWN_PROCESSED" in results

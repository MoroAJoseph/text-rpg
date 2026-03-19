from unittest.mock import MagicMock
from engine.api.events import EventsAPI
from engine.core.enums import EventTypeEnum


def test_events_api_proxies_subscriptions():
    engine = MagicMock()
    api = EventsAPI(engine)
    callback = lambda e: print(e)

    api.on_type(EventTypeEnum.INPUT, callback)

    engine.ctx.bus.subscribe_to_type.assert_called_with(EventTypeEnum.INPUT, callback)

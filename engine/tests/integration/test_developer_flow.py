from engine import (
    create_engine,
    connect,
    EngineOptions,
    ConnectionCapability,
    EventData,
    EventTypeEnum,
    SystemEventEnum,
)


def test_full_developer_flow():
    # 1. Setup
    options = EngineOptions()
    engine_instance = create_engine(options)
    api = connect(
        engine_instance, [ConnectionCapability.SYSTEM, ConnectionCapability.EVENTS]
    )

    # 2. Track internal state
    results = {"started": False, "custom_received": False}

    def on_start(event: EventData):
        results["started"] = True
        api.events.emit(
            EventData(type=EventTypeEnum.SYSTEM, name=SystemEventEnum.ENGINE_TICK)
        )

    def on_tick(event: EventData):
        results["custom_received"] = True

    # 3. Subscribe
    api.events.on(SystemEventEnum.ENGINE_START, on_start)
    api.events.on(SystemEventEnum.ENGINE_TICK, on_tick)

    # 4. Trigger
    api.system.start()

    # 5. Process - Using the instance-specific bus
    engine_instance.ctx.bus.process()  # Handles START -> Emits TICK
    engine_instance.ctx.bus.process()  # Handles TICK

    # 6. Verify
    assert results["started"] is True
    assert results["custom_received"] is True

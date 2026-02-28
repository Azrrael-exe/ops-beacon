from src.infrastructure.mqtt_client.mqtt import MQTTProcessor, Route
from asyncio import run
from src.application.use_cases.real_time_even_processor import RealTimeEventProcessor, event_parser
from src.infrastructure.repositories.memory import MemoryFastEventRepository
from src.infrastructure.dummies import DummyAlertService, DummyDisplayService
from src.infrastructure.rules.simple import SimpleRule

processor = MQTTProcessor(
    hostname="broker.hivemq.com",
    port=1883,
    # username="admin",
    # password="admin",
    routes=[
        Route(
            topic="ops-beacon/events",
            handler=RealTimeEventProcessor(
                event_repository=MemoryFastEventRepository(),
                rule=SimpleRule(),
                alert_service=DummyAlertService(),
                display_service=DummyDisplayService()
            ).process,
            dto=event_parser
        )
    ]
)

if __name__ == "__main__":
    run(processor.main())
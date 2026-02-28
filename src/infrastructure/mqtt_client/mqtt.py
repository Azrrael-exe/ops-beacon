from aiomqtt import Client
from dataclasses import dataclass
from typing import Callable, Any
import json

from logging import getLogger

logger = getLogger(__name__)

@dataclass
class Route:
    topic: str
    handler: Callable[[list[Any]], None]
    dto: Callable[[dict[str, Any]], Any]


class MQTTProcessor:
    def __init__(
        self,
        hostname: str,
        port: int = 1883,
        username: str | None = None,
        password: str | None = None,
        routes: list[Route] = None
    ):
        self.__hostname = hostname
        self.__port = port
        self.__username = username
        self.__password = password
        self.__routes = routes or []

    async def main(self):
        async with Client(
            hostname=self.__hostname,
            port=self.__port,
            username=self.__username,
            password=self.__password
        ) as client:
            # Subscribe to all topics within the async context
            for route in self.__routes:
                await client.subscribe(route.topic)
                logger.info(f"Subscribed to topic: {route.topic}")

            async for message in client.messages:
                for route in self.__routes:
                    if message.topic.matches(route.topic):
                        try:
                            payload = json.loads(message.payload.decode())
                            parsed_data = route.dto(payload)
                            route.handler(parsed_data)
                            logger.info(f"Handled message from {message.topic}")
                        except Exception as e:
                            logger.error(f"Error handling message: {e}")
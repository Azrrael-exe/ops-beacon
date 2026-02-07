from enum import Enum, auto
from datetime import datetime
from typing import Any

class EventLevel(Enum):
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()

class EventStatus(Enum):
    NEW = auto()
    ACKNOWLEDGED = auto()
    RESOLVED = auto()


class Event:
    def __init__(
        self,
        id: int,
        source: str,
        level: EventLevel,
        timestamp: datetime,
        status: EventStatus = EventStatus.NEW,
        should_alert: bool = False,
        metadata: dict = {},
    ):
        self.__id = id
        self.__source = source
        self.__metadata = metadata
        self.__level = level
        self.__timestamp = timestamp
        self.__status = status
        self.__ack_timestamp = None
        self.__resolved_timestamp = None
        self.__should_alert = False
    
    @property
    def id(self) -> int:
        return self.__id
    
    @property
    def source(self) -> str:
        return self.__source
    
    @property
    def metadata(self) -> dict:
        return self.__metadata
    
    @property
    def level(self) -> EventLevel:
        return self.__level
    
    @property
    def timestamp(self) -> datetime:
        return self.__timestamp
    
    @property
    def status(self) -> EventStatus:
        return self.__status
    
    @property
    def should_alert(self) -> bool:
        return self.__should_alert
    
    @property
    def ack_timestamp(self) -> datetime | None:
        return self.__ack_timestamp
    
    @property
    def resolved_timestamp(self) -> datetime | None:
        return self.__resolved_timestamp
    
    def is_acknowledged(self) -> bool:
        return self.__status in [EventStatus.ACKNOWLEDGED, EventStatus.RESOLVED]
    
    def is_resolved(self) -> bool:
        return self.__status == EventStatus.RESOLVED
    
    def resolve(self) -> None:
        if self.__status == EventStatus.ACKNOWLEDGED:
            self.__status = EventStatus.RESOLVED
            self.__resolved_timestamp = datetime.now()
        else:
            raise ValueError("Event is not acknowledged")
    
    def acknowledge(self) -> None:
        if self.__status == EventStatus.NEW:   
            self.__status = EventStatus.ACKNOWLEDGED
            now = datetime.now()
            if self.__timestamp <= now:
                self.__ack_timestamp = now
            else:
                raise ValueError("Event timestamp is in the future")
        else:
            raise ValueError("Event is not new")

    def add_metadata(self, key: str, value: Any) -> dict:
        self.__metadata[key] = value
        return self.__metadata
    
    def set_as_alerting(self) -> None:
        self.__should_alert = True

    def __repr__(self) -> str:
        return f"Event(id={self.id}, source={self.source}, metadata={self.metadata}, level={self.level}, timestamp={self.timestamp}, status={self.status}, ack_timestamp={self.ack_timestamp}, resolved_timestamp={self.resolved_timestamp})"
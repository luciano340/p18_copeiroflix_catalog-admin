from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import uuid

from src.core._shared.events.abstract_message_bus import AbstractMessageBus
from src.core._shared.events.message_bus import MessageBus
from src.core._shared.notification import Notification
from src.core._shared.events.event import Event


@dataclass(kw_only=True)
class Entity(ABC):
    id:  uuid.UUID = field(default_factory=uuid.uuid4)
    notificaiton: Notification = field(default_factory=Notification, init=False)
    events: list[Event] = field(default_factory=list, init=False)
    message_bus: AbstractMessageBus = field(default_factory=MessageBus, compare=False)
    
    def dispatch(self, event: Event) -> None:
        self.events.append(event)
        self.message_bus.handle(self.events)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id
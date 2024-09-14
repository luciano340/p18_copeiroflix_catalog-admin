from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import uuid

from src.core._shared.notification import Notification


@dataclass(kw_only=True)
class Entity(ABC):
    id:  uuid.UUID = field(default_factory=uuid.uuid4)
    notificaiton: Notification = field(default_factory=Notification)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id
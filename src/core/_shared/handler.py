from abc import ABC, abstractmethod
from sched import Event


class Handler(ABC):
    @abstractmethod
    def handle(self, event: Event) -> None:
        pass
from abc import ABC, abstractmethod


class AbstractConsumer(ABC):
    @abstractmethod
    def on_message(self, message: bytes) -> None:
        pass

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass
from abc import ABC, abstractmethod


class StorageServiceInterface(ABC):

    @abstractmethod
    def store(self, path: str, content: bytes, type: str):
        raise NotImplementedError
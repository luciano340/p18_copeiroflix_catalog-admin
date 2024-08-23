from abc import ABC, abstractmethod


class CategoryRepositoryInterface(ABC):
    @abstractmethod
    def save(self, category):
        raise NotImplementedError
    
    def get_by_id(self, id):
        raise NotImplementedError
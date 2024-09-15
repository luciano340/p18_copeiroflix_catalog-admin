from abc import ABC, abstractmethod
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMember

class CastMemberRepositoryInterface(ABC):
    @abstractmethod
    def save(self, castmember: CastMember) -> CastMember:
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> CastMember | None:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self,id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, castmember: CastMember) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(self, order_by: str) -> list[CastMember]:
        raise NotImplementedError
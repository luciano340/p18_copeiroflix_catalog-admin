from uuid import UUID
from src.core.cast_member.domain.cast_member import CastMember
from src.core.category.domain.category_repository_interface import CategoryRepositoryInterface

class InMemoryCastMemberRepository(CategoryRepositoryInterface):
    def __init__(self, castmembers=None) -> None:
        self.castmembers = castmembers or []
    
    def save(self, cast_member: CastMember) -> None:
        self.castmembers.append(cast_member)
    
    def get_by_id(self, id: UUID) -> CastMember | None:
        for c in self.castmembers:
            if c.id == id:
                return c
        return None

    def delete_by_id(self, id: UUID) -> None:
        for n, i in enumerate(self.castmembers):
            if i.id == id:
                self.castmembers.pop(n)
    
    def update(self, cast_member: CastMember) -> None:
        for n, i in enumerate(self.castmembers):
            if i.id == cast_member.id:
                self.castmembers[n] = cast_member

    def list(self) -> list[CastMember]:
        return [c for c in self.castmembers]
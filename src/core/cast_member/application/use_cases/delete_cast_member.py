
from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.application.use_cases.exceptions import CastMemberNotFound
from src.core.cast_member.domain.cast_member_repository_interface import CastMemberRepositoryInterface


@dataclass
class DeleteCastMemberRequest:
    id: UUID


class DeleteCastMember:
    def __init__(self, repository: CastMemberRepositoryInterface) -> None:
        self.repository = repository
    
    def execute(self, request: DeleteCastMemberRequest):
        cast_member = self.repository.get_by_id(id=request.id)

        if cast_member is None:
            raise CastMemberNotFound(f"CastMember with id {request.id} not found for delete")
        
        self.repository.delete_by_id(id=request.id)


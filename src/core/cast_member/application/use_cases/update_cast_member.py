


from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.application.use_cases.exceptions import CastMemberNotFound
from src.core.cast_member.domain import cast_member
from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository_interface import CastMemberRepositoryInterface


@dataclass
class UpdateCastMemberRequest:
    id: UUID
    name: str | None = None
    type: CastMemberType | None = None
    
class UpdateCastMember:
    def __init__(self, repository: CastMemberRepositoryInterface):
        self.repository = repository

    def execute(self, request: UpdateCastMemberRequest) -> None:
        cast_member = self.repository.get_by_id(request.id)
        
        if cast_member is None:
            raise CastMemberNotFound(f"CastMember with id {request.id} not found for update")
        
        current_name = cast_member.name
        current_type = cast_member.type

        if request.name:
            current_name = request.name

        if request.type:
            current_type = request.type
        
        cast_member.update_cast_member(name=current_name, type=current_type)
        
        self.repository.update(castmember=cast_member)
        
        
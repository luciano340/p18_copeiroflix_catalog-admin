from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

from src.core.cast_member.application.use_cases.exceptions import CastMemberNotFound
from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository_interface import CastMemberRepositoryInterface


@dataclass
class GetCastMemberRequest:
    id: UUID

@dataclass
class GetCastMemberResponse:
    id: UUID
    name: str
    type: CastMemberType
    created_date: datetime
    updated_date: datetime

class GetCastMember:
    def __init__(self, repository: CastMemberRepositoryInterface) -> None:
        self.repository = repository
    
    def execute(self, request: GetCastMemberRequest) -> GetCastMemberResponse:
        CastMember = self.repository.get_by_id(id=request.id)

        if CastMember:
            return GetCastMemberResponse(
                id=CastMember.id,
                name=CastMember.name,
                type=CastMember.type,
                created_date=CastMember.created_date,
                updated_date=CastMember.updated_date
            )
        
        raise CastMemberNotFound(f"CastMember with id {request.id} not found")


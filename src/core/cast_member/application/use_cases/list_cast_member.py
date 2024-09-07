
from dataclasses import dataclass
import datetime
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository_interface import CastMemberRepositoryInterface


@dataclass
class CastMemberOutput:
    id: UUID
    name: str
    type: CastMemberType
    created_date: datetime
    updated_date: datetime
    
@dataclass
class RequestListCastMember:
    pass

@dataclass
class ResponseListCastMember:
    data: list[CastMemberOutput]

class ListCastMember():
    def __init__(self, repository: CastMemberRepositoryInterface) -> None:
        self.repository = repository
    
    def execute(self, request: RequestListCastMember) -> ResponseListCastMember:
        CastMembers = self.repository.list()
        mapped_CastMembers = [
            CastMemberOutput(
                id=cm.id,
                name=cm.name,
                type=cm.type,
                created_date=cm.created_date,
                updated_date=cm.updated_date
            ) for cm in CastMembers
        ]
        return ResponseListCastMember(data=mapped_CastMembers)
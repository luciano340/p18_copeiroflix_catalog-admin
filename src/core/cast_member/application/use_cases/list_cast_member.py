
from dataclasses import dataclass
import datetime
from uuid import UUID
from django.core.exceptions import FieldError

from src.core.cast_member.application.use_cases.exceptions import CastMemberOrderNotFound
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
    order_by: str = "name"

@dataclass
class ResponseListCastMember:
    data: list[CastMemberOutput]

class ListCastMember():
    def __init__(self, repository: CastMemberRepositoryInterface) -> None:
        self.repository = repository
    
    def execute(self, request: RequestListCastMember) -> ResponseListCastMember:
        try:
            CastMembers = self.repository.list(order_by=request.order_by)
        except FieldError:
            raise CastMemberOrderNotFound(f'Filed {request.order_by} not found')
        
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
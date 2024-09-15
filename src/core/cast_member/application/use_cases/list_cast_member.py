
from dataclasses import dataclass, field
import datetime
import os
from uuid import UUID
from django.core.exceptions import FieldError

from src.core._shared.dto import ListOuputMeta
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
    current_page: int = 1

@dataclass
class ResponseListCastMember:
    data: list[CastMemberOutput]
    meta: ListOuputMeta = field(default_factory=ListOuputMeta)

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

        DEFAULT_PAGE_SIZE = os.environ.get("page_size", 5)
        page_offset = (request.current_page - 1) * DEFAULT_PAGE_SIZE
        castmembers_page = mapped_CastMembers[page_offset:page_offset + DEFAULT_PAGE_SIZE]

        return ResponseListCastMember(
            data=castmembers_page,
            meta=ListOuputMeta(
                current_page=request.current_page,
                page_size=DEFAULT_PAGE_SIZE,
                total=len(castmembers_page)
            )
        )
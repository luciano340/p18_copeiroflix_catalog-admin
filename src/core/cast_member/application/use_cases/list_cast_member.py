
from dataclasses import dataclass, field
import datetime
import os
from uuid import UUID
from django.core.exceptions import FieldError

from src._shared.logger import get_logger
from src.core._shared.dto import ListOuputMeta
from src.core._shared.factory_pagination import CreateListPagination
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
        self.logger = get_logger(__name__)
        self.logger.debug(f'Iniciando instâcia {self.repository}')
        
    def execute(self, request: RequestListCastMember) -> ResponseListCastMember:
        self.logger.info('Iniciando listagem de membros do elenco')
        self.logger.debug(f'Argumentos {request} - {type(request)}')
        try:
            CastMembers = self.repository.list(order_by=request.order_by)
        except FieldError:
            self.logger.error(f'Erro na ordenação, coluna {request.order_by} não localizada')
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

        self.logger.debug(f'Membros do elenco localizadas {mapped_CastMembers}')
        castmembers_page = CreateListPagination.configure_pagination(
            mapped_list=mapped_CastMembers, 
            current_page=request.current_page
        )

        return ResponseListCastMember(
            data=castmembers_page,
            meta=ListOuputMeta(
                current_page=request.current_page,
                page_size=os.environ.get("page_size", 5),
                total=len(castmembers_page)
            )
        )
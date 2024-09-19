from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

from src._shared.logger import get_logger
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
        self.logger = get_logger(__name__)
        self.logger.debug(f'instância iniciada com {repository} - {type(repository)}')
    
    def execute(self, request: GetCastMemberRequest) -> GetCastMemberResponse:
        self.logger.info(f'Iniciando busca de membro do elenco {request.id}')
        self.logger.debug(f'Argumentos {request} - {type(request)}')
        CastMember = self.repository.get_by_id(id=request.id)

        if CastMember:
            self.logger.info(f'Membro do elenco {request.id} localizado')
            self.logger.debug(f'Membro do Elenco {request.id} localizado - Informações vindas do banco: {CastMember} - {type(CastMember)}')
            return GetCastMemberResponse(
                id=CastMember.id,
                name=CastMember.name,
                type=CastMember.type,
                created_date=CastMember.created_date,
                updated_date=CastMember.updated_date
            )
        
        self.logger.error(f"Membro do elenco {request.id} não localizado")
        raise CastMemberNotFound(f"CastMember with id {request.id} not found")


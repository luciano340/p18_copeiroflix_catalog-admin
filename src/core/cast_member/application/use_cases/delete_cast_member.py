
from dataclasses import dataclass
from uuid import UUID

from src._shared.logger import get_logger
from src.core.cast_member.application.use_cases.exceptions import CastMemberNotFound
from src.core.cast_member.domain.cast_member_repository_interface import CastMemberRepositoryInterface


@dataclass
class DeleteCastMemberRequest:
    id: UUID


class DeleteCastMember:
    def __init__(self, repository: CastMemberRepositoryInterface) -> None:
        self.repository = repository
        self.logger = get_logger(__name__)
        self.logger.debug(f'instância iniciada com {repository} - {type(repository)}')
        
    def execute(self, request: DeleteCastMemberRequest):
        self.logger.info(f'Iniciando deleção de membro do elenco {request.id}')
        self.logger.debug(f'Argumentos {request} - {type(request)}')
        cast_member = self.repository.get_by_id(id=request.id)

        if cast_member is None:
            self.logger.error(f"Não foi possível localizar o membro do elenco {request.id} para deleção")
            raise CastMemberNotFound(f"CastMember with id {request.id} not found for delete")
        
        self.repository.delete_by_id(id=request.id)
        self.logger.info(f'Membro do elenco {request.id} deletado')


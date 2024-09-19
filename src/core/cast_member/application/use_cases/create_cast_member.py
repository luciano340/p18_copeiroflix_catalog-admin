from dataclasses import dataclass
from uuid import UUID
from src._shared.logger import get_logger
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository_interface import CastMemberRepositoryInterface
from src.core.cast_member.application.use_cases.exceptions import InvalidCastMemberData

@dataclass
class CreateCastMemberRequest:
    name: str
    type: CastMemberType = None

@dataclass
class CreateCastMemberResponse:
    id: UUID

class CreateCastMember:
    def __init__(self, repository: CastMemberRepositoryInterface) -> CreateCastMemberResponse:
        self.repository = repository
        self.logger = get_logger(__name__)
        self.logger.debug(f'instância iniciada com {repository} - {type(repository)}')

    def execute(self, request: CreateCastMemberRequest) -> CreateCastMemberResponse:
        self.logger.info(f'Iniciando criação de membro do elenco {request.name}')
        self.logger.debug(f'Argumentos {request} - {type(request)}')
        try:
            cast_member = CastMember(
                name=request.name,
                type=request.type
            )
        except ValueError as err:
            self.logger.error(f"Os argumentos repassados são inválidos {err}")
            raise InvalidCastMemberData(err)

        self.repository.save(cast_member)
        self.logger.debug(f'Dados a serem persistidos {cast_member}')
        self.logger.info('Criação do membro do elenco finalizada')
        return CreateCastMemberResponse(
            id=cast_member.id
        )
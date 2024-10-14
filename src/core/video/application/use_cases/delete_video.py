from dataclasses import dataclass
from uuid import UUID

from src._shared.logger import get_logger
from src.core.video.application.use_cases.exceptions import VideoNotFound
from src.core.video.domain.video_repository_interface import VideoRepositoryInterface


@dataclass
class DeleteVideoRequest:
    id: UUID

class DeleteVideo:
    def __init__(self, repository: VideoRepositoryInterface) -> None:
        self.repository = repository
        self.logger = get_logger(__name__)
        self.logger.debug(f'instância iniciada com {repository} - {type(repository)}')
        
    def execute(self, request: DeleteVideoRequest):
        self.logger.info(f'Iniciando deleção do video {request.id}')
        self.logger.debug(f'Argumentos {request} - {type(request)}')
        video = self.repository.get_by_id(id=request.id)

        if video is None:
            self.logger.error(f"Não foi possível localizar o genero {request.id} para deleção")
            raise VideoNotFound(f"Video with id {request.id} not found for delete")
        
        self.repository.delete_by_id(id=request.id)
        self.logger.info(f'Video {request.id} deletado')


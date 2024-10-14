
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from uuid import UUID

from src._shared.logger import get_logger
from src.core._shared.infra.storage.storage_service_interface import StorageServiceInterface
from src.core.video.application.use_cases.exceptions import AudioVideoMediaError, VideoNotFound
from src.core.video.domain.value_objetcs import ImageMedia, ImageMediaType
from src.core.video.domain.video_repository_interface import VideoRepositoryInterface


@dataclass
class RequestUploadImage:
    video_id: UUID
    file_name: str
    content: bytes
    content_type: str
    image_type: ImageMediaType

@dataclass
class ResponseUploadImage:
    pass

class UploadImage:
    def __init__(self, video_repository: VideoRepositoryInterface, storage_service: StorageServiceInterface):
        self.video_repository = video_repository
        self.storage_service = storage_service
        self.logger = get_logger(__name__)
        self.logger.debug(f'instância iniciada com {video_repository} - {type(video_repository)}')

    def execute(self, request: RequestUploadImage) -> ResponseUploadImage:
        self.logger.info(f'Iniciando upload do imagem {request.file_name} em {request.video_id}')
        video = self.video_repository.get_by_id(id=request.video_id)

        if video is None:
            self.logger.error(f"Video com id {request.video_id} não encontrado!")
            raise VideoNotFound(f"Video com id {request.video_id} não encontrado!")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path= Path("images")/ str(video.id) / f"{timestamp}_{request.file_name}"

        self.storage_service.store(
            path=str(file_path),
            content=request.content,
            type=request.content_type
        )

        self.logger.debug('upload finalizado no usecase')

        audio_video_mnedia = ImageMedia(
            name=request.file_name,
            location=str(file_path),
            type=request.image_type
        )

        self.logger.debug(f"Tipo de media localizada {request.image_type}")
        try:
            if request.image_type == ImageMediaType.BANNER:
                video.update_banner(audio_video_mnedia)
            elif request.image_type == ImageMediaType.THUMBNAIL:
                video.update_thumbnail(audio_video_mnedia)
            elif request.image_type == ImageMediaType.THUMBNAIL_HALF:
                video.update_thumbnail_half(audio_video_mnedia)
            else:
                raise AudioVideoMediaError(f"Tipo de media inválida {request.image_type}")
    
            self.logger.debug(f'Entidade atualizada {video}')
            try:
                self.video_repository.update(video=video)
            except Exception as err:
                self.logger.error('aqui 1 {err}')
            
            try:
                    self.video_repository.update_image(video=video, image_type=request.image_type)
            except Exception as err:
                self.logger.error(f"ue {err}")
        except Exception as err:
            self.logger.error(f'Erro ao atualizar AudioMedia {err}')
            raise AudioVideoMediaError(err)
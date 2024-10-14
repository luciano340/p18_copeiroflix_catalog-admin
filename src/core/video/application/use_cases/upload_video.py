from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from uuid import UUID
from src._shared.logger import get_logger
from src.core._shared.infra.storage.storage_service_interface import StorageServiceInterface
from src.core.video.application.use_cases.exceptions import AudioVideoMediaError, VideoNotFound
from src.core.video.domain.value_objetcs import AudioMediaType, AudioVideoMedia, MediaStatus
from src.core.video.domain.video_repository_interface import VideoRepositoryInterface

@dataclass
class RequestUploadVideo:
    video_id: UUID
    file_name: str
    content: bytes
    content_type: str
    video_type: AudioMediaType

@dataclass
class ResponseUploadVideo:
    pass

class UploadVideo:
    def __init__(self, video_repository: VideoRepositoryInterface, storage_service: StorageServiceInterface):
        self.video_repository = video_repository
        self.storage_service = storage_service
        self.logger = get_logger(__name__)
        self.logger.debug(f'instância iniciada com {video_repository} - {type(video_repository)}')

    def execute(self, request: RequestUploadVideo) -> ResponseUploadVideo:
        self.logger.info(f'Iniciando upload do video {request.file_name} em {request.video_id}')
        try:
            video = self.video_repository.get_by_id(id=request.video_id)
            
            if video is None:
                self.logger.error(f"Video com id {request.video_id} não encontrado!")
                raise VideoNotFound(f"Video com id {request.video_id} não encontrado!")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path= Path("videos")/ str(video.id) / f"{timestamp}_{request.file_name}"
            
            self.storage_service.store(
                path=str(file_path),
                content=request.content,
                type=request.content_type
            )

            self.logger.debug('upload finalizado no usecase')

            audio_video_mnedia = AudioVideoMedia(
                name=request.file_name,
                raw_location=str(file_path),
                encoded_location=None,
                status=MediaStatus.PENDING,
                type=request.video_type
            )
        except Exception as err:
            self.logger.error('aqui {err}')

        self.logger.debug(f"Tipo de media localizada {request.video_type}")
        try:
            if request.video_type == AudioMediaType.VIDEO:
                video.update_video(audio_video_mnedia)
            elif request.video_type == AudioMediaType.TRAILER:
                video.update_trailer(audio_video_mnedia)
            else:
                raise AudioVideoMediaError(f"Tipo de media inválida {request.video_type}")
    
            self.logger.debug(f'Entidade atualizada {video}')
            self.video_repository.update(video=video)
            self.video_repository.update_media(video=video, video_type=request.video_type)
        except Exception as err:
            self.logger.error(f'Erro ao atualizar AudioMedia {err}')
            raise AudioVideoMediaError(err)
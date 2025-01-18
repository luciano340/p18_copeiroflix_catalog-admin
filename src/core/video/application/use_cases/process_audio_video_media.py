from dataclasses import dataclass
from uuid import UUID

from src._shared.logger import get_logger
from src.core.video.application.use_cases.exceptions import MediaNotFound, VideoNotFound
from src.core.video.domain.value_objetcs import AudioMediaType, MediaStatus
from src.core.video.domain.video_repository_interface import VideoRepositoryInterface


@dataclass
class ProcessAudioVideoMediaOutput:
    pass

@dataclass
class ProcessAudioVideoMediaInput:
    encoded_path: str
    video_id: UUID
    status: MediaStatus
    media_type: AudioMediaType

class ProcessAudioVideoMedia:
    def __init__(self, video_repository: VideoRepositoryInterface) -> None:
        self.repository = video_repository
        self.logger = get_logger(__name__)
        self.logger.debug(f'instância iniciada com {video_repository} - {type(video_repository)}')

    def execute(self, request: ProcessAudioVideoMediaInput) -> ProcessAudioVideoMediaOutput:
        video = self.repository.get_by_id(id=request.video_id)

        if video is None:
            self.logger.error(f"Video com ID {request.video_id} não encontrado")
            raise VideoNotFound(f"Video com ID {request.video_id} não encontrado")
            
        audio_media_instance = getattr(video, request.media_type.value.lower(), None)
        if not audio_media_instance:
            self.logger.error(f"O {request.media_type.value} deve ter uma media para ser processado!")
            raise MediaNotFound(f"O {request.media_type.value} deve ter uma media para ser processado!")
        
        video.process(status=request.status, encoded_location=request.encoded_path, media_type=request.media_type)
        
        self.repository.update(video)
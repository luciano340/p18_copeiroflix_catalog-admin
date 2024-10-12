
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
import os
from uuid import UUID
from django.core.exceptions import FieldError

from src._shared.logger import get_logger
from src.core._shared.dto import ListOuputMeta
from src.core._shared.factory_pagination import CreateListPagination
from src.core.video.application.use_cases.exceptions import VideoOrderNotFound
from src.core.video.domain.value_objetcs import AudioMediaType, ImageMedia, MediaStatus, Rating
from src.core.video.domain.video_repository_interface import VideoRepositoryInterface
from src.django_project.apps.video.models import AudioVideoMedia as AudioVideoMediaORM

@dataclass
class AudioVideoMediaOutput:
    id: UUID
    name: str
    raw_location: str
    encoded_location: str | None
    status: MediaStatus
    type: AudioMediaType

@dataclass
class VideoOutput:
    id: UUID
    title: str
    description: str
    duration: Decimal
    rating: Rating
    banner: ImageMedia | None
    thumbnail: ImageMedia | None
    thumbnail_half: ImageMedia | None
    trailer: AudioVideoMediaOutput | None
    video: AudioVideoMediaOutput | None
    categories: set[UUID]
    genres: set[UUID]
    cast_members: set[UUID]
    created_date: datetime
    updated_date: datetime
    launch_at: datetime
    published: bool = False

@dataclass
class RequestListVideo:
    order_by: str = "title"
    current_page: int = 1

@dataclass
class ResponseListVideo:
    data: list[VideoOutput]
    meta: ListOuputMeta = field(default_factory=ListOuputMeta)

class ListVideo():
    def __init__(self, repository: VideoRepositoryInterface) -> None:
        self.repository = repository
        self.logger = get_logger(__name__)
        self.logger.debug(f'Iniciando instâcia {self.repository}')
        
    def execute(self, request: RequestListVideo) -> ResponseListVideo:
        self.logger.info('Iniciando listagem de generos')
        self.logger.debug(f'Argumentos {request} - {type(request)}')
        try:
            videos = self.repository.list(order_by=request.order_by)
        except FieldError:
            self.logger.error(f'Erro na ordenação, coluna {request.order_by} não localizada')
            raise VideoOrderNotFound(f'Field {request.order_by} not found')

        mapped_videos = [
            VideoOutput(
                id=v.id,
                title=v.title,
                description=v.description,
                duration=v.duration,
                rating=v.rating,
                banner=v.banner,
                thumbnail=v.thumbnail,
                thumbnail_half=v.thumbnail_half,
                trailer=self.__map_audio_video_media(v.trailer),
                video=self.__map_audio_video_media(v.video),
                categories=v.categories,
                genres=v.genres,
                cast_members=v.cast_members,
                created_date=v.created_date,
                updated_date=v.updated_date,
                launch_at=v.launch_at,
                published=v.published
            ) for v in videos
        ]
        
        debug = [{r.id: r.video} for r in mapped_videos]
        self.logger.debug(f'Videos localizados {debug}')
        videos_page = CreateListPagination.configure_pagination(
            mapped_list=mapped_videos, 
            current_page=request.current_page
        )

        return ResponseListVideo(
            data=videos_page,
            meta=ListOuputMeta(
                current_page=request.current_page,
                page_size=os.environ.get("page_size", 5),
                total=len(mapped_videos)
            )
        )
    
    def __map_audio_video_media(self, media: AudioVideoMediaORM) -> AudioVideoMediaOutput:
        if media is None:
            return None
        
        mapped_media = AudioVideoMediaOutput(
            id=media.id,
            name=media.name,
            raw_location=media.raw_location if media.raw_location else None,
            encoded_location=media.encoded_location if media.encoded_location else None,
            status=media.status,
            type=media.type
        )
        
        return mapped_media
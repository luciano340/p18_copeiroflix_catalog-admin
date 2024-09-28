from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from src._shared.logger import get_logger
from src.core._shared.notification import Notification
from src.core.cast_member.domain.cast_member_repository_interface import CastMemberRepositoryInterface
from src.core.category.domain.category_repository_interface import CategoryRepositoryInterface
from src.core.genre.domain.genre_repository_interface import GenreRepositoryInterface
from src.core.video.application.use_cases.exceptions import InvalidVideo, RelatedEntitiesNotFound
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository_interface import VideoRepositoryInterface



@dataclass
class RequestCreateVideoWithoutMedia:
    title: str
    description: str
    duration: Decimal
    launch_at: datetime | None = None
    rating: str
    categories: set[UUID]
    genres: set[UUID]
    cast_members: set[UUID]

@dataclass
class ResponseCreateVideoWithoutMedia:
    id: UUID

class CreateVideoWithoutMedia:
    def __init__(
              self, 
              video_repository: VideoRepositoryInterface,
              category_repository: CategoryRepositoryInterface,
              genre_repository: GenreRepositoryInterface,
              cast_member_repository: CastMemberRepositoryInterface,
              ) -> None:
        self.video_repository = video_repository
        self.category_repository = category_repository
        self.genre_repository = genre_repository
        self.cast_member_repository = cast_member_repository
        self.logger = get_logger(__name__)
        self.logger.debug(f'instância iniciada com {video_repository} - {type(video_repository)} - {category_repository} - {genre_repository} - {cast_member_repository}')
        
    def execute(self, request: ResponseCreateVideoWithoutMedia) -> ResponseCreateVideoWithoutMedia:
        self.logger.info(f'Iniciando criação devideo sem midia {request.name}')
        self.logger.debug(f'Argumentos {request} - {type(request)}')
        notification = Notification()
        self._validate_categories(request=request, notificaiton=notification)
        self._validate_genres(request=request, notificaiton=notification)
        self._validate_cast_members(request=request, notificaiton=notification)

        if notification.has_errors:
            raise RelatedEntitiesNotFound(notification.messages)

        try:
            video = Video(
                title=request.title,
                description=request.description,
                duration=request.duration,
                rating=request.rating,
                launch_at=request.launch_at,
                published=False,
                categories=request.categories,
                genres=request.genres,
                cast_members=request.cast_members
            )
        except ValueError as err:
            self.logger.error(f'Entidade Video invalida {err}')
            raise InvalidVideo(err)
        
        self.video_repository.save(video=video)

    def _validate_categories(self, request: RequestCreateVideoWithoutMedia, notificaiton: Notification) -> None:
        categories_ids = {category.id for category in self.category_repository.list()}

        if not request.categories.issubset(categories_ids):
            self.logger.error(f'Não foi possível localizar a categorias vinculada ao video {request.title} - {request.categories - categories_ids}')
            notificaiton.add_error(f"Categories ID not found: {request.categories - categories_ids}")

    def _validate_genres(self, request: RequestCreateVideoWithoutMedia, notificaiton: Notification) -> None:
        genres_ids = {genre.id for genre in self.genre_repository.list()}

        if not request.genres.issubset(genres_ids):
            self.logger.error(f'Não foi possível localizar os generos vinculada ao video {request.title} - {request.genres - genres_ids}')
            notificaiton.add_error(f"Categories ID not found: {request.title} - {request.genres - genres_ids}")

    def _validate_cast_members(self, request: RequestCreateVideoWithoutMedia, notificaiton: Notification) -> None:
        cast_members_ids = {cm.id for cm in self.cast_member_repository.list()}

        if not request.cast_members.issubset(cast_members_ids):
            self.logger.error(f'Não foi possível localizar a categorias vinculada ao genero {request.title} - {request.cast_members - cast_members_ids}')
            notificaiton.add_error(f"Categories ID not found: {request.cast_members - cast_members_ids}")
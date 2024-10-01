
from uuid import UUID
from django.db import transaction

from src.core.video.domain.video import Video
from src.core.video.domain.video_repository_interface import VideoRepositoryInterface
from src.django_project.apps.video.models import Video as VideoORM

class DjangoORMVideoRepository(VideoRepositoryInterface):

    def save(self, video: Video) -> Video:
        with transaction.atomic():
            video_model = VideoModelMapper.to_model(video)
            video_model.save()
            video_model.categories.set(video.categories)
            video_model.genres.set(video.genres)
            video_model.cast_members.set(video.cast_members)

    def get_by_id(self, id: UUID) -> Video | None:
        try:
            genre_model = VideoORM.objects.get(id=id)
        except:
            return None
        return VideoModelMapper.to_entity(genre_model)

    def delete_by_id(self,id: UUID) -> None:
        VideoORM.objects.filter(id=id).delete()

    def update(self, video: Video) -> None:
        try:
            video_model = VideoORM.objects.get(id=video.id)
        except VideoORM.DoesNotExist:
            return None
    
        with transaction.atomic():
            VideoORM.objects.filter(id=video.id).update(
                title=video.title,
                description=video.description,
                duration=video.duration,
                rating=video.rating,
                banner=video.banner,
                thumbnail=video.thumbnail,
                thumbnail_half=video.thumbnail_half,
                trailer=video.trailer,
                video=video.video,
                launch_at=video.launch_at,
                published=video.published,
                updated_date=video.updated_date
            )
            video_model.categories.set(video.categories)
            video_model.genres.set(video.genres)
            video_model.cast_members.set(video.cast_members)

    def list(self, order_by: str = "title") -> list[Video]:
        genre_list = [
            VideoModelMapper.to_entity(genre_model)
            for genre_model in VideoORM.objects.all().order_by(order_by)
        ]

        return genre_list

class VideoModelMapper:
    @staticmethod
    def to_model(video: Video) -> VideoORM:
        video_model = VideoORM(
                title=video.title,
                description=video.description,
                duration=video.duration,
                rating=video.rating,
                banner=video.banner,
                thumbnail=video.thumbnail,
                thumbnail_half=video.thumbnail_half,
                trailer=video.trailer,
                video=video.video,
                launch_at=video.launch_at,
                published=video.published,
                updated_date=video.updated_date,
                created_date=video.created_date,

        )
        video_model.save()
        video_model.categories.set(video.categories)
        video_model.genres.set(video.genres)
        video_model.cast_members.set(video.cast_members)
        
        return video_model

    @staticmethod
    def to_entity(video_model: VideoORM) -> Video:
        return Video(
            title=video_model.title,
            description=video_model.description,
            duration=video_model.duration,
            rating=video_model.rating,
            banner=video_model.banner,
            thumbnail=video_model.thumbnail,
            thumbnail_half=video_model.thumbnail_half,
            trailer=video_model.trailer,
            video=video_model.video,
            launch_at=video_model.launch_at,
            published=video_model.published,
            updated_date=video_model.updated_date,
            created_date=video_model.created_date,
            categories={c.id for c in video_model.categories.all()},
            cast_members={c.id for c in video_model.cast_members.all()},
            genres={c.id for c in video_model.genres.all()}
        )
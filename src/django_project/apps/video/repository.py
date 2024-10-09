
from uuid import UUID
from django.db import transaction

from src.core.video.domain.value_objetcs import AudioMediaType, ImageMedia, ImageMediaType
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository_interface import VideoRepositoryInterface
from src.django_project.apps.video.exceptions import AudioMediaEmptyORM
from src.django_project.apps.video.models import Video as VideoORM, AudioVideoMedia

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
            video_model = VideoORM.objects.get(id=id)
        except VideoORM.DoesNotExist as err:
            return None
        return VideoModelMapper.to_entity(video_model)

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
                launch_at=video.launch_at,
                published=video.published,
                updated_date=video.updated_date
            )
            video_model.categories.set(video.categories)
            video_model.genres.set(video.genres)
            video_model.cast_members.set(video.cast_members)
    
    def update_media(self, video: Video):
        try:
            video_model = VideoORM.objects.get(id=video.id)
        except VideoORM.DoesNotExist:
            return None

        if video.video is None:
            raise AudioMediaEmptyORM(f"The video of the entity {video} cannot be empty for update")

        AudioVideoMedia.objects.filter(id=video_model.id, type=AudioMediaType.VIDEO).delete()
        
        video_model.video = AudioVideoMedia.objects.create(
            name=video.video.name,
            raw_location=video.video.raw_location,
            status=video.video.status,
            type=AudioMediaType.VIDEO
        )

        video_model.save()

    def update_trailer(self, video: Video):
        try:
            video_model = VideoORM.objects.get(id=video.id)
        except VideoORM.DoesNotExist:
            return None

        if video.video is None:
            raise AudioMediaEmptyORM(f"The trailer of the entity {video} cannot be empty for update")

        AudioVideoMedia.objects.filter(id=video_model.id, type=AudioMediaType.TRAILER).delete()
        
        video_model.trailer = AudioVideoMedia.objects.create(
            name=video.video.name,
            raw_location=video.video.raw_location,
            status=video.video.status,
            type=AudioMediaType.TRAILER
        )

        video_model.save()

    def update_banner(self, video: Video):
        try:
            video_model = VideoORM.objects.get(id=video.id)
        except VideoORM.DoesNotExist:
            return None

        if video.video is None:
            raise AudioMediaEmptyORM(f"The banner of the entity {video} cannot be empty for update")

        ImageMedia.objects.filter(id=video_model.id, type=ImageMediaType.BANNER).delete()
        
        video_model.banner = ImageMedia.objects.create(
            name=video.banner.name,
            location=video.banner.location,
            type=ImageMediaType.BANNER
        )

        video_model.save()

    def update_thumbnail(self, video: Video):
        try:
            video_model = VideoORM.objects.get(id=video.id)
        except VideoORM.DoesNotExist:
            return None

        if video.video is None:
            raise AudioMediaEmptyORM(f"The thumbnail of the entity {video} cannot be empty for update")

        ImageMedia.objects.filter(id=video_model.id, type=ImageMediaType.THUMBNAIL).delete()
        
        video_model.banner = ImageMedia.objects.create(
            name=video.banner.name,
            location=video.banner.location,
            type=ImageMediaType.THUMBNAIL
        )

        video_model.save()

    def update_thumbnail_half(self, video: Video):
        try:
            video_model = VideoORM.objects.get(id=video.id)
        except VideoORM.DoesNotExist:
            return None

        if video.video is None:
            raise AudioMediaEmptyORM(f"The thumbnail_half of the entity {video} cannot be empty for update")

        ImageMedia.objects.filter(id=video_model.id, type=ImageMediaType.THUMBNAIL_HALF).delete()
        
        video_model.banner = ImageMedia.objects.create(
            name=video.banner.name,
            location=video.banner.location,
            type=ImageMediaType.THUMBNAIL_HALF
        )

        video_model.save()
          
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
            id=video.id,
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
            id=video_model.id,
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
            categories=set(video_model.categories.values_list("id", flat=True)),
            cast_members=set(video_model.cast_members.values_list("id", flat=True)),
            genres=set(video_model.genres.values_list("id", flat=True))
        )
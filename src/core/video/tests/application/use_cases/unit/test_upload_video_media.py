from unittest.mock import create_autospec
import uuid

from freezegun import freeze_time
from src.core._shared.events.abstract_message_bus import AbstractMessageBus
from src.core._shared.infra.storage.storage_service_interface import StorageServiceInterface
from src.core.video.application.use_cases.events.integration_events import AudioVideoMediaUpdatedIntegrationEvent
from src.core.video.application.use_cases.upload_video import RequestUploadVideo, UploadVideo
from src.core.video.domain.value_objetcs import AudioMediaType, AudioVideoMedia, MediaStatus, Rating
from src.core.video.domain.video import Video
from src.core.video.infra.in_memory_video_repository import InMemoryVideoRepository


class TesteUploadMediaVideo:
    def test_upload_video_media(self):
        video = Video(
            title="Teste",
            description="Teste 2222",
            duration=250.5,
            rating=Rating.L,
            categories=set([uuid.uuid4()]),
            genres=set([uuid.uuid4()]),
            cast_members=set([uuid.uuid4()])
        )

        video_repository = InMemoryVideoRepository(videos=[video])
        mock_storage = create_autospec(StorageServiceInterface)
        mock_message_bus = create_autospec(AbstractMessageBus)

        with freeze_time("2024-04-04 20:20:20"):
            use_case = UploadVideo(video_repository=video_repository, storage_service=mock_storage, message_bus=mock_message_bus)
            request = RequestUploadVideo(
                video_id=video.id,
                file_name="meuvideo.mp4",
                content=b"asd8hjasudhasd",
                content_type="video/mp4",
                video_type=AudioMediaType.VIDEO
            )
            use_case.execute(request=request)

        mock_storage.store.assert_called_once_with(
            path=f"videos\\{video.id}\\VIDEO\\20240404_202020_meuvideo.mp4",
            content=b"asd8hjasudhasd",
            type="video/mp4",
        )

        repo_video = video_repository.get_by_id(id=video.id)
        assert repo_video.video == AudioVideoMedia(
            name="meuvideo.mp4",
            raw_location=f"videos\\{video.id}\\VIDEO\\20240404_202020_meuvideo.mp4",
            encoded_location=None,
            status=MediaStatus.PENDING,
            type=AudioMediaType.VIDEO
        )
        mock_message_bus.handle.assert_called_once_with(
            [
                AudioVideoMediaUpdatedIntegrationEvent(
                    resource_id=video.id,
                    file_path=f"videos\\{video.id}\\VIDEO\\20240404_202020_meuvideo.mp4",
                    type=AudioMediaType.VIDEO
                )
            ]
        )
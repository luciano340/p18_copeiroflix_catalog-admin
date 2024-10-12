import os
from unittest.mock import create_autospec
import uuid

from src.core._shared.dto import ListOuputMeta
from src.core.video.application.use_cases.list_video import ListVideo, RequestListVideo, ResponseListVideo, VideoOutput
from src.core.video.domain.value_objetcs import Rating
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository_interface import VideoRepositoryInterface


class TestListVideo:
    def test_list_all_videos_with_success(self):
        video_repository = create_autospec(VideoRepositoryInterface)
        category_id    = uuid.uuid4()
        cast_member_id = uuid.uuid4()
        genre_id       = uuid.uuid4()

        video = Video(
            title="Johnny M - Let's Go Deeper",
            description="Welcome to this Deep House journey",
            duration=120,
            rating=Rating.L,
            categories=set([category_id]),
            genres=set([genre_id]),
            cast_members=set([cast_member_id]),
            published=True
        )

        video_repository.list.return_value = [video]

        use_case = ListVideo(repository=video_repository)
        output = use_case.execute(request=RequestListVideo())
        assert output == ResponseListVideo(
            data=[
                VideoOutput(
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
                    categories=video.categories,
                    genres=video.genres,
                    cast_members=video.cast_members,
                    created_date=video.created_date,
                    updated_date=video.updated_date,
                    launch_at=video.launch_at,
                    published=video.published
                )
            ],
            meta=ListOuputMeta(
                current_page=1,
                page_size=os.environ.get("page_size", 5),
                total=1
            )
        )

    def test_when_no_genres_exist_then_return_empty_data(self):
        video_repository = create_autospec(VideoRepositoryInterface)
        video_repository.list.return_value = []

        use_case = ListVideo(repository=video_repository)
        output = use_case.execute(request=RequestListVideo())

        assert output == ResponseListVideo(data=[], meta=ListOuputMeta(current_page=1, page_size=os.environ.get("page_size", 5), total=0))
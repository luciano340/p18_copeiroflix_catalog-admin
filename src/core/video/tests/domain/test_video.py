from os import name
import uuid

from freezegun import freeze_time
import pytest
from src.core.video.domain.events.events import AudioVideoMediaUpdated
from src.core.video.domain.value_objetcs import AudioMediaType, AudioVideoMedia, MediaStatus
from src.core.video.domain.video import Video


class TestVideo:
    def test_create_a_valid_entity(self):
        with freeze_time("2024-09-21 08:08:08"):
            video = Video(
                title="Filme",
                description="É um filme",
                duration=200,
                published=False,
                rating="L",
                categories=set([uuid.uuid4()]),
                genres=set([uuid.uuid4()]),
                cast_members=set([uuid.uuid4()])
            )
        
        assert video.title == "Filme"
        assert video.description == "É um filme"
        assert video.duration == 200
        assert video.rating == "L"
        assert video.updated_date == None
        assert video.created_date == "2024-09-21 08:08:08"
        assert str(video.launch_at) == "2024-09-21"
    
    def test_create_invalid_entity_without_title(self):
        with pytest.raises(ValueError, match="Title cannot be empty"):
            video = Video(
                title="",
                description="É um filme",
                duration=200,
                published=False,
                rating="L",
                categories=set([uuid.uuid4()]),
                genres=set([uuid.uuid4()]),
                cast_members=set([uuid.uuid4()])
            )
    
    def test_create_invalid_entity_title_greater_then_255(self):
        with pytest.raises(ValueError, match="Title must have less than 255 characteres"):
            video = Video(
                title="a"*300,
                description="É um filme",
                duration=200,
                published=False,
                rating="L",
                categories=set([uuid.uuid4()]),
                genres=set([uuid.uuid4()]),
                cast_members=set([uuid.uuid4()])
            )
    
    def test_create_invalid_entity_duration_less_then_0(self):
        with pytest.raises(ValueError, match="Duration must greater then zero"):
            video = Video(
                title="File",
                description="É um filme",
                duration=-1,
                published=False,
                rating="L",
                categories=set([uuid.uuid4()]),
                genres=set([uuid.uuid4()]),
                cast_members=set([uuid.uuid4()])
            )

    def test_create_invalid_entity_no_category(self):
        with pytest.raises(ValueError, match="The movie must be at least one category"):
            video = Video(
                title="File",
                description="É um filme",
                duration=200,
                published=False,
                rating="L",
                categories=[],
                genres=set([uuid.uuid4()]),
                cast_members=set([uuid.uuid4()])
            )
    
    def test_create_invalid_entity_no_genres(self):
        with pytest.raises(ValueError, match="The movie must be at least one genre"):
            video = Video(
                title="File",
                description="É um filme",
                duration=200,
                published=False,
                rating="L",
                categories=set([uuid.uuid4()]),
                genres=[],
                cast_members=set([uuid.uuid4()])
            )

    def test_create_invalid_entity_no_cast_members(self):
        with pytest.raises(ValueError, match="The movie must be at least one cast_member"):
            video = Video(
                title="File",
                description="É um filme",
                duration=200,
                published=False,
                rating="L",
                categories=set([uuid.uuid4()]),
                genres=set([uuid.uuid4()]),
                cast_members=[]
            )

    def test_update_cast_members(self):
        video = Video(
            title="File",
            description="É um filme",
            duration=200,
            published=False,
            rating="L",
            categories=set([uuid.uuid4()]),
            genres=set([uuid.uuid4()]),
            cast_members=set([uuid.uuid4()])
        )

        assert len(video.cast_members) == 1
        video.add_cast_member(cast_member=uuid.uuid4())
        assert len(video.cast_members) == 2
        
        cm_list = [uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
        video.add_cast_member(cast_member=cm_list)
        assert len(video.cast_members) == 5

    def test_update_video_media_anbd_dispatch_event(self):
        video = Video(
            title="Filme",
            description="É um filme",
            duration=200,
            published=False,
            rating="L",
            categories=set([uuid.uuid4()]),
            genres=set([uuid.uuid4()]),
            cast_members=set([uuid.uuid4()])
        )

        media = AudioVideoMedia(
            name=f"{video.title}.mp4",
            raw_location="raw_path",
            encoded_location="encoded_path",
            status=MediaStatus.COMPLETED,
            type=AudioMediaType.VIDEO
        )
        video.update_video(video=media)
        
        assert video.video == media
        assert video.events == [
            AudioVideoMediaUpdated(
                aggregate_id=video.id,
                file_path=media.raw_location,
                media_type=media.type
            )
        ]
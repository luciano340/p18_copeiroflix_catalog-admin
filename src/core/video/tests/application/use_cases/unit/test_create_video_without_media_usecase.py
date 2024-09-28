from unittest.mock import MagicMock, create_autospec
import uuid
import pytest

from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository_interface import CastMemberRepositoryInterface
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository_interface import CategoryRepositoryInterface
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository_interface import GenreRepositoryInterface
from src.core.video.application.use_cases.create_video_without_media import CreateVideoWithoutMedia, RequestCreateVideoWithoutMedia
from src.core.video.application.use_cases.exceptions import InvalidVideo, RelatedEntitiesNotFound
from src.core.video.domain.video_repository_interface import VideoRepositoryInterface




class TestCreateCastMember:
    def test_create_video_with_valid_data(self):
        mock_repository_video = MagicMock(VideoRepositoryInterface)
        mock_repository_category = MagicMock(CategoryRepositoryInterface)
        category = Category(name="Movie")
        mock_repository_category.list.return_value = [category]
        mock_repository_genre = MagicMock(GenreRepositoryInterface)
        genre = Genre(name="Terror")
        mock_repository_genre.list.return_value = [genre]
        mock_repository_cast_member = MagicMock(CastMemberRepositoryInterface)
        cast_member = CastMember(name="Robert", type="CONVIDADO")
        mock_repository_cast_member.list.return_value = [cast_member]

        use_case = CreateVideoWithoutMedia(
            video_repository=mock_repository_video,
            category_repository=mock_repository_category,
            genre_repository=mock_repository_genre,
            cast_member_repository=mock_repository_cast_member
        )

        video_request = RequestCreateVideoWithoutMedia(
                title="Creepy Nuts",
                description="「Bling-Bang-Bang-Born」",
                duration=2.52,
                launch_at="2021-09-28",
                rating="L",
                categories=set([category.id]),
                genres=set([genre.id]),
                cast_members=set([cast_member.id])
        )
        video_response = use_case.execute(request=video_request)
        assert isinstance(video_response.id, uuid.UUID)
        mock_repository_video.save.assert_called_once()
    
    def test_create_video_with_invalid_data(self):
        mock_repository_video = MagicMock(VideoRepositoryInterface)
        mock_repository_category = MagicMock(CategoryRepositoryInterface)
        category = Category(name="Movie")
        mock_repository_category.list.return_value = [category]
        mock_repository_genre = MagicMock(GenreRepositoryInterface)
        genre = Genre(name="Terror")
        mock_repository_genre.list.return_value = [genre]
        mock_repository_cast_member = MagicMock(CastMemberRepositoryInterface)
        cast_member = CastMember(name="Robert", type="CONVIDADO")
        mock_repository_cast_member.list.return_value = [cast_member]

        use_case = CreateVideoWithoutMedia(
            video_repository=mock_repository_video,
            category_repository=mock_repository_category,
            genre_repository=mock_repository_genre,
            cast_member_repository=mock_repository_cast_member
        )

        video_request = RequestCreateVideoWithoutMedia(
                title="",
                description="「Bling-Bang-Bang-Born」",
                duration=2.52,
                launch_at="2021-09-28",
                rating="L",
                categories=set([category.id]),
                genres=set([genre.id]),
                cast_members=set([cast_member.id])
        )

        with pytest.raises(InvalidVideo):
            use_case.execute(request=video_request)

    def test_create_video_with_invalid_related_entites(self):
        mock_repository_video = MagicMock(VideoRepositoryInterface)
        mock_repository_category = MagicMock(CategoryRepositoryInterface)
        mock_repository_genre = MagicMock(GenreRepositoryInterface)
        mock_repository_cast_member = MagicMock(CastMemberRepositoryInterface)

        use_case = CreateVideoWithoutMedia(
            video_repository=mock_repository_video,
            category_repository=mock_repository_category,
            genre_repository=mock_repository_genre,
            cast_member_repository=mock_repository_cast_member
        )

        video_request = RequestCreateVideoWithoutMedia(
                title="",
                description="「Bling-Bang-Bang-Born」",
                duration=2.52,
                launch_at="2021-09-28",
                rating="L",
                categories=set([uuid.uuid4()]),
                genres=set([uuid.uuid4()]),
                cast_members=set([uuid.uuid4()])
        )

        with pytest.raises(RelatedEntitiesNotFound):
            use_case.execute(request=video_request)
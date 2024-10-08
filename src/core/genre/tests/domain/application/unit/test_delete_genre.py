import uuid
from unittest.mock import create_autospec
import pytest
from src.core.genre.application.use_cases.delete_genre import DeleteGenre, DeleteGenreRequest
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository_interface import GenreRepositoryInterface


class TestDeleteGenre:
    @pytest.fixture
    def mock_genre_repository(self) -> GenreRepositoryInterface:
        return create_autospec(GenreRepositoryInterface)

    def test_delete_genre_from_repository(self, mock_genre_repository):
        genre = Genre(name="Drama")
        mock_genre_repository.get_by_id.return_value = genre

        use_case = DeleteGenre(repository=mock_genre_repository)

        use_case.execute(DeleteGenreRequest(id=genre.id))

        mock_genre_repository.delete_by_id.assert_called_once_with(id=genre.id)

    def test_when_genre_does_not_exist_then_raise_error(self, mock_genre_repository):
        mock_genre_repository.get_by_id.return_value = None

        use_case = DeleteGenre(repository=mock_genre_repository)

        with pytest.raises(Exception, match="Genre with id .* not found"):
            use_case.execute(DeleteGenreRequest(id=uuid.uuid4()))
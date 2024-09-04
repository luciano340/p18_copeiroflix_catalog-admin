from unittest.mock import create_autospec
import uuid
import pytest
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository_interface import CategoryRepositoryInterface
from src.core.genre.application.use_cases.create_genre import CreateGenre, CreateGenreRequest
from src.core.genre.application.use_cases.exceptions import InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository_interface import GenreRepositoryInterface


@pytest.fixture
def mock_genre_repository() -> GenreRepositoryInterface:
    return create_autospec(GenreRepositoryInterface)

@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")

@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")


@pytest.fixture
def mock_category_repository_with_categories(movie_category, documentary_category) -> CategoryRepositoryInterface:
    repository = create_autospec(CategoryRepositoryInterface)
    repository.list.return_value = [movie_category, documentary_category]
    return repository

@pytest.fixture
def mock_empty_category_repository() -> CategoryRepositoryInterface:
    repository = create_autospec(CategoryRepositoryInterface)
    repository.list.return_value = []
    return repository

class TestCreateGenre:
    def test_when_categories_do_not_exist_then_raise_error(
            self,
            mock_empty_category_repository,
            mock_genre_repository
    ) -> None:
        use_case = CreateGenre(
            repository=mock_genre_repository,
            category_repository=mock_empty_category_repository
        )
        input = CreateGenreRequest(name="Ação", categories_ids={uuid.uuid4()})

        with pytest.raises(RelatedCategoriesNotFound):
            use_case.execute(input)

    def test_when_created_genre_is_invalid_then_raise_error(
            self,
            movie_category,
            mock_category_repository_with_categories,
            mock_genre_repository
    ) -> None:
        use_case = CreateGenre(
            repository=mock_genre_repository,
            category_repository=mock_category_repository_with_categories
        )
        input = CreateGenreRequest(name="", categories_ids={movie_category.id})

        with pytest.raises(InvalidGenre):
            use_case.execute(input)

    def test_when_created_genre_is_valid_and_save_with_categories(
            self,
            movie_category,
            documentary_category,
            mock_category_repository_with_categories,
            mock_genre_repository
    ) -> None:
        use_case = CreateGenre(
            repository=mock_genre_repository,
            category_repository=mock_category_repository_with_categories
        )
        input = CreateGenreRequest(name="Terror", categories_ids={movie_category.id, documentary_category.id})

        response = use_case.execute(request=input)

        genre = Genre(
            id=response.id,
            name="Terror",
            is_active=True,
            categories={movie_category.id, documentary_category.id}
        )

        mock_genre_repository.save.assert_called_once_with(genre)
        assert isinstance(response.id, uuid.UUID )

    def test_created_genre_without_categories(
            self,
            mock_category_repository_with_categories,
            mock_genre_repository
    ) -> None:
        use_case = CreateGenre(
            repository=mock_genre_repository,
            category_repository=mock_category_repository_with_categories
        )
        input = CreateGenreRequest(name="Terror")

        response = use_case.execute(request=input)

        genre = Genre(
            id=response.id,
            name="Terror",
            is_active=True,
            categories=set()
        )

        mock_genre_repository.save.assert_called_once_with(genre)
        assert isinstance(response.id, uuid.UUID )
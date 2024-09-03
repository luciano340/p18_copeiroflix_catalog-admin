from unittest.mock import create_autospec
import uuid

from freezegun import freeze_time
import pytest
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository_interface import CategoryRepositoryInterface
from src.core.genre.application.use_cases.exceptions import GenreNotFound, RelatedCategoriesInvalid, RelatedCategoriesNotFound
from src.core.genre.application.use_cases.update_genre import UpdateGenre, UpdateGenreRequest
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository_interface import GenreRepositoryInterface



class TestListGenre:
    def test_update_fail_when_genre_does_not_exists(self):
        genre_repository = create_autospec(GenreRepositoryInterface)
        genre_repository.get_by_id.return_value = None
        category_repository = create_autospec(CategoryRepositoryInterface)
        category_repository.get_by_id.return_value = None

        use_case = UpdateGenre(repository=genre_repository, categoryRepository=category_repository)

        request_dto = UpdateGenreRequest(
            id=uuid.uuid4(),
            name="Drama",
            is_active=False
        )

        with pytest.raises(GenreNotFound):
            use_case.execute(request=request_dto)
    
    def test_update_with_invalid_category_id(self):
        genre = Genre(
            name="Terror"
        )
        genre_repository = create_autospec(GenreRepositoryInterface)
        genre_repository.get_by_id.return_value = genre
        category_repository = create_autospec(CategoryRepositoryInterface)
        category_repository.get_by_id.return_value = None
        use_case = UpdateGenre(repository=genre_repository, categoryRepository=category_repository)

        request_dto = UpdateGenreRequest(
            id=genre.id,
            name="Drama",
            is_active=False,
            categories_id={'asdfasdas'}
        )

        with pytest.raises(RelatedCategoriesInvalid):
            use_case.execute(request=request_dto) 

    def test_update_fail_category_id_not_found(self):
        genre = Genre(
            name="Terror"
        )
        genre_repository = create_autospec(GenreRepositoryInterface)
        genre_repository.get_by_id.return_value = genre
        category_repository = create_autospec(CategoryRepositoryInterface)
        category_repository.get_by_id.return_value = None
        use_case = UpdateGenre(repository=genre_repository, categoryRepository=category_repository)

        request_dto = UpdateGenreRequest(
            id=genre.id,
            name="Drama",
            is_active=False,
            categories_id={uuid.uuid4()}
        )

        with pytest.raises(RelatedCategoriesNotFound):
            use_case.execute(request=request_dto)
    
    def test_update_all(self):
        genre = Genre(
            name="Terror",
            is_active=True,
            categories={}
        )
        
        category = Category(
            name="Filme",
            description="Teste de filme",
            is_active=True
        )

        genre_repository = create_autospec(GenreRepositoryInterface)
        genre_repository.get_by_id.return_value = genre
        category_repository = create_autospec(CategoryRepositoryInterface)
        category_repository.get_by_id.return_value = category
        use_case = UpdateGenre(repository=genre_repository, categoryRepository=category_repository)

        request_dto = UpdateGenreRequest(
            id=genre.id,
            name="Drama",
            is_active=False,
            categories_id={category.id}
        )

        with freeze_time("2023-09-03 20:20:20"):
            use_case.execute(request=request_dto)

        assert genre.name == "Drama"
        assert genre.is_active == False
        assert genre.categories == {category.id}
        assert genre.updated_date == "2023-09-03 20:20:20"
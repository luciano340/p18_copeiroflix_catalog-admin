
from rest_framework.test import APIClient
from rest_framework import status
import pytest

from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.django_project.apps.category.repository import DjangoORMCategoryRepository
from src.django_project.apps.genre.repository import DjangoORMGenreRepository


@pytest.fixture
def category_movie() -> Category:
    return Category(
        name="Filme",
        description="Filme muito louco"
    )

@pytest.fixture
def category_doc() -> Category:
    return Category(
        name="Documentário",
        description="Documentário muito louco"
    )

@pytest.fixture
def category_repository(category_movie, category_doc) -> DjangoORMCategoryRepository:
    repository = DjangoORMCategoryRepository()
    repository.save(category_movie)
    repository.save(category_doc)
    return repository

@pytest.fixture
def genre_repository() -> DjangoORMGenreRepository:
    return DjangoORMGenreRepository()

@pytest.fixture
def genre_terror(category_doc, category_movie) -> Genre:
    return Genre(
        name="Terror",
        is_active=True,
        categories={category_doc.id, category_movie.id}
    )

@pytest.fixture
def genre_drama() -> Genre:
    return Genre(
        name="Drama"
    )

@pytest.mark.django_db
class TestListAPI:
    def test_list_genres_and_categories(
            self,
            genre_repository,
            category_repository,
            genre_terror,
            genre_drama,
            category_doc,
            category_movie
    ):
        genre_repository.save(genre_terror)
        genre_repository.save(genre_drama)

        url = "/api/genres/"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]
        assert response.data["data"][0]["id"] == str(genre_terror.id)
        assert response.data["data"][0]["name"] == genre_terror.name
        assert response.data["data"][0]["is_active"] == genre_terror.is_active
        assert set(response.data["data"][0]["categories_id"]) == {
            str(category_doc.id),
            str(category_movie.id)
        }

        assert response.data["data"]
        assert response.data["data"][1]["id"] == str(genre_drama.id)
        assert response.data["data"][1]["name"] == genre_drama.name
        assert response.data["data"][1]["is_active"] == genre_drama.is_active
        assert response.data["data"][1]["categories_id"] == []
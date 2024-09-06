
from freezegun import freeze_time
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
    

@pytest.mark.django_db
class TestCreateAPI:
    def test_create_genre_with_categories(
            self,
            genre_repository: DjangoORMGenreRepository,
            category_repository,
            category_movie,
            category_doc
    ):
        repo_category = category_repository
        print(repo_category.list())

        url = "/api/genres/"

        with freeze_time("2024-09-06 07:24:00"):
            response = APIClient().post(
                url,
                data={
                    "name": "Terror",
                    "is_active": "True",
                    "categories_id": [
                        f"{category_movie.id}",
                        f"{category_doc.id}"
                    ]
                }
            )

        print(response.data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"]
        assert len(genre_repository.list()) == 1
        genre_from_repository = genre_repository.get_by_id(id=response.data["id"])
        assert str(genre_from_repository.id) == response.data["id"]
        assert genre_from_repository.name == "Terror"
        assert genre_from_repository.is_active == True
        assert genre_from_repository.categories == {category_movie.id, category_doc.id}
        assert str(genre_from_repository.created_date) == "2024-09-06 07:24:00+00:00"
        assert genre_from_repository.updated_date == None
    
@pytest.mark.django_db
class TestDelteAPI:
    def test_delete_genre(
            self,
            genre_repository: DjangoORMGenreRepository,
            genre_drama
    ):
        genre_repository.save(genre_drama)

        url = f"/api/genres/{genre_drama.id}/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert len(genre_repository.list()) == 0
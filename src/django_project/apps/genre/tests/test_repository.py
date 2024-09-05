from re import I
from freezegun import freeze_time
import pytest

from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.django_project.apps.category.repository import DjangoORMCategoryRepository
from src.django_project.apps.genre.repository import DjangoORMGenreRepository
from src.django_project.apps.genre.models import Genre as GenreORM

@pytest.mark.django_db
class TestRepositoryGenre:
    def test_save_genre_in_database(self):
        with freeze_time("2024-04-04 04:04:04"):
            genre = Genre(name="Terror")
        genre_repository = DjangoORMGenreRepository()

        assert GenreORM.objects.count() == 0
        genre_repository.save(genre=genre)

        assert GenreORM.objects.count() == 1
        genre_model = GenreORM.objects.first()
        assert genre_model.id == genre.id
        assert genre_model.name == genre.name
        assert genre_model.is_active == genre.is_active
        assert genre_model.categories.count() == 0
        assert genre_model.created_date.strftime("%Y-%m-%d %H:%M:%S") == "2024-04-04 04:04:04"
        assert genre_model.updated_date == None
    
    def test_save_genre_with_categories(self):
        repository = DjangoORMGenreRepository()
        category_repository = DjangoORMCategoryRepository()

        category = Category(name="Filme", description="Filmes")
        category_repository.save(category=category)

        with freeze_time("2024-05-04 04:04:04"):
            genre = Genre(
                name="Drama",
                is_active=True,
                categories={category.id}
            )

        assert GenreORM.objects.count() == 0
        repository.save(genre=genre)

        assert GenreORM.objects.count() == 1
        genre_model = GenreORM.objects.first()
        assert genre_model.id == genre.id
        assert genre_model.name == genre.name
        assert genre_model.is_active == genre.is_active
        genre_model.categories.get().id == category.id
        assert genre_model.categories.count() == 1
        assert genre_model.created_date.strftime("%Y-%m-%d %H:%M:%S") == "2024-05-04 04:04:04"
        assert genre_model.updated_date == None
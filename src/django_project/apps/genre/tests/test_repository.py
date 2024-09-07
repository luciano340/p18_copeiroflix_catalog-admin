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
    
    def test_delete_genre(self):
        repository = DjangoORMGenreRepository()
        genre = Genre(
            name="Drama",
            is_active=True,
            categories={}
        )

        assert GenreORM.objects.count() == 0
        repository.save(genre=genre)
        assert GenreORM.objects.count() == 1
        repository.delete_by_id(id=genre.id)
        assert GenreORM.objects.count() == 0
    
    def test_get_genre_by_id(self):
        repository = DjangoORMGenreRepository()
        genre1 = Genre(
            name="Drama",
            is_active=True,
            categories={}
        )

        genre2 = Genre(
            name="Terror",
            is_active=False,
            categories={}
        )
        repository.save(genre=genre1)
        repository.save(genre=genre2)
        
        genre_from_orm = repository.get_by_id(id=genre1.id)

        assert isinstance(genre_from_orm, Genre)
        assert genre_from_orm.id == genre1.id
        assert genre_from_orm.name == genre1.name
        assert genre_from_orm.is_active == genre1.is_active
    
    def test_get_all_genres(self):
        repository = DjangoORMGenreRepository()
        category_repository = DjangoORMCategoryRepository()

        category = Category(name="Filme", description="Filmes")
        category_repository.save(category=category)

        genre1 = Genre(
            name="Drama",
            is_active=True,
            categories={}
        )

        genre2 = Genre(
            name="Terror",
            is_active=False,
            categories={category.id}
        )

        assert GenreORM.objects.count() == 0
        repository.save(genre=genre1)
        repository.save(genre=genre2)

        assert GenreORM.objects.count() == 2

        list_of_genres = repository.list()     

        assert len(list_of_genres) == 2
        assert list_of_genres[0].id == genre1.id
        assert list_of_genres[0].name == genre1.name
        assert list_of_genres[0].is_active == genre1.is_active
        assert len(list_of_genres[0].categories) == 0
        assert list_of_genres[1].id == genre2.id
        assert list_of_genres[1].name == genre2.name
        assert list_of_genres[1].is_active == genre2.is_active
        assert len(list_of_genres[1].categories) == 1
        assert list_of_genres[1].categories == {category.id}
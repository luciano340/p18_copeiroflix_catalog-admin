from uuid import UUID
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository_interface import GenreRepositoryInterface
from django.db import transaction
from src.django_project.apps.genre.models import Genre as GenreORM
class DjangoORMGenreRepository(GenreRepositoryInterface):

    def save(self, genre: Genre) -> Genre:
        with transaction.atomic():
            genre_model = CategoryModelMapper.to_model(genre)
            genre_model.save()
            genre_model.categories.set(genre.categories)
    
    def get_by_id(self, id: UUID) -> Genre | None:
        try:
            genre_model = GenreORM.objects.get(id=id)
        except:
            return None
        return CategoryModelMapper.to_entity(genre_model)

    def delete_by_id(self,id: UUID) -> None:
        GenreORM.objects.filter(id=id).delete()

    def update(self, genre: Genre) -> None:
        try:
            genre_model = GenreORM.objects.get(id=genre.id)
        except GenreORM.DoesNotExist:
            return None
    
        with transaction.atomic():
            GenreORM.objects.filter(id=genre.id).update(
                name=genre.name,
                is_active=genre.is_active,
                updated_date=genre.updated_date
            )
            genre_model.categories.set(genre.categories)

    def list(self) -> list[Genre]:
        genre_list = [
            CategoryModelMapper.to_entity(genre_model)
            for genre_model in GenreORM.objects.all()
        ]

        return genre_list

class CategoryModelMapper:
    @staticmethod
    def to_model(genre: Genre) -> GenreORM:
        return GenreORM(
            id=genre.id,
            name=genre.name,
            is_active=genre.is_active,
            created_date=genre.created_date,
            updated_date=genre.updated_date
        )

    @staticmethod
    def to_entity(genre_model: GenreORM) -> Genre:
        return Genre(
            id=genre_model.id,
            name=genre_model.name,
            is_active=genre_model.is_active,
            categories={c.id for c in genre_model.categories.all()},
            created_date=genre_model.created_date,
            updated_date=genre_model.updated_date
        )
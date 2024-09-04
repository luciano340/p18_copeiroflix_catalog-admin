from os import name
from freezegun import freeze_time
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.application.use_cases.exceptions import RelatedCategoriesNotFound
from src.core.genre.application.use_cases.update_genre import UpdateGenre, UpdateGenreRequest
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository

class TestUpdateGenre:
    def test_update_genre_with_associated_categories(self):
        category_repository = InMemoryCategoryRepository()
        genre_repository = InMemoryGenreRepository()

        category_1 = Category(name="Category 1", description="Category 1 description")
        category_2 = Category(name="Category 2", description="Category 2 description")
        category_repository.save(category_1)
        category_repository.save(category_2)

        with freeze_time("2024-01-01 20:20:20"):
            genre = Genre(
                name="Drama",
                is_active=True,
                categories={}
            )
        genre_repository.save(genre)

        use_case = UpdateGenre(
            repository=genre_repository,
            categoryRepository=category_repository,
        )

        request_dto = UpdateGenreRequest(
            id=genre.id,
            name="Terror",
            is_active=False,
            categories_id={category_1.id, category_2.id}
        )

        with freeze_time("2024-01-02 19:19:19"):
            use_case.execute(request=request_dto)
        
        updated_genre = genre_repository.get_by_id(id=genre.id)

        assert updated_genre.id == genre.id
        assert updated_genre.name == "Terror"
        assert updated_genre.categories == {category_1.id, category_2.id}
        assert updated_genre.updated_date == "2024-01-02 19:19:19"
        assert updated_genre.created_date == "2024-01-01 20:20:20"


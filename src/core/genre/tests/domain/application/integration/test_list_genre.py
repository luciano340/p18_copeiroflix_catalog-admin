from freezegun import freeze_time
from src.core._shared.dto import ListOuputMeta
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.application.use_cases import list_genre
from src.core.genre.application.use_cases.list_genre import GenreOutput, ListGenre, RequestListGenre, ResponseListGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


class TestListGenre:
    def test_list_genres_with_categories(self):
        genre_repository = InMemoryGenreRepository()
        category_repository = InMemoryCategoryRepository()

        movie_category = Category(
            name="Filme",
            description="Descrição de filme"
        )
        category_repository.save(movie_category)
        documentary_category = Category(
            name="Documentário",
            description="Descrição do documentário"
        )
        category_repository.save(documentary_category)
        with freeze_time("2024-09-03 07:07:07"):
            genre = Genre(
                name="Terror",
                categories={movie_category.id, documentary_category.id}
            )
        genre_repository.save(genre)

        use_case = ListGenre(repository=genre_repository)
        response = use_case.execute(request=RequestListGenre())

        print(f'{response.data}')
        assert len(response.data) == 1
        assert response == ResponseListGenre(
            data=[
                GenreOutput(
                    id=genre.id,
                    name=genre.name,
                    is_active=genre.is_active,
                    categories_id={movie_category.id, documentary_category.id},
                    created_date="2024-09-03 07:07:07",
                    updated_date=None
                )
            ],
            meta=ListOuputMeta(current_page=1, page_size=5, total=1)
        )

        


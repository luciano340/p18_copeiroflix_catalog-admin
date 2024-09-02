import uuid
from unittest.mock import create_autospec

from freezegun import freeze_time

from src.core.genre.application.use_cases.list_genre import ListGenre, GenreOutput, RequestListGenre, ResponseListGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository_interface import GenreRepositoryInterface


class TestListGenre:
    def test_list_genres_with_associated_categories(self):
        genre_repository = create_autospec(GenreRepositoryInterface)

        cat_1_id = uuid.uuid4()
        cat_2_id = uuid.uuid4()

        with freeze_time("2024-09-03 07:07:07"):
            genre_drama = Genre(
                name="Drama",
                categories={cat_1_id, cat_2_id},
            )
        with freeze_time("2024-09-04 07:07:07"):
            genre_romance = Genre(name="Romance")

        genre_repository.list.return_value = [genre_drama, genre_romance]

        use_case = ListGenre(repository=genre_repository)
        output = use_case.execute(RequestListGenre())

        assert output == ResponseListGenre(
            data=[
                GenreOutput(
                    id=genre_drama.id,
                    name="Drama",
                    categories_id={cat_1_id, cat_2_id},
                    is_active=True,
                    created_date="2024-09-03 07:07:07",
                    updated_date=None
                ),
                GenreOutput(
                    id=genre_romance.id,
                    name="Romance",
                    categories_id=set(),
                    is_active=True,
                    created_date="2024-09-04 07:07:07",
                    updated_date=None
                ),
            ]
        )

    def test_when_no_genres_exist_then_return_empty_data(self):
        genre_repository = create_autospec(GenreRepositoryInterface)
        genre_repository.list.return_value = []

        use_case = ListGenre(repository=genre_repository)
        output = use_case.execute(RequestListGenre())

        assert output == ResponseListGenre(data=[])
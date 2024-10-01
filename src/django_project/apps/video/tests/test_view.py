from uuid import UUID
import uuid
from freezegun import freeze_time
import pytest
from rest_framework.test import APIClient
from rest_framework import status

from src.core.cast_member.domain.cast_member import CastMember
from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.django_project.apps.cast_member.repository import DjangoORMCastMemberRepository
from src.django_project.apps.category.repository import DjangoORMCategoryRepository
from src.django_project.apps.genre.repository import DjangoORMGenreRepository
from src.django_project.apps.video.repository import DjangoORMVideoRepository


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
def castmember_samuel() -> CastMember:
    return CastMember(
        name="Samuel",
        type="APRESENTADOR"
    )

@pytest.fixture
def genre_terror(category_movie) -> Genre:
    return Genre(
        name="Terror",
        categories=set([category_movie.id])
    )

@pytest.fixture
def castmember_repository(castmember_samuel) -> DjangoORMCastMemberRepository:
    repository = DjangoORMCastMemberRepository()
    repository.save(castmember_samuel)
    return repository

@pytest.fixture
def category_repository(category_movie, category_doc) -> DjangoORMCategoryRepository:
    repository = DjangoORMCategoryRepository()
    repository.save(category_movie)
    repository.save(category_doc)
    return repository

@pytest.fixture
def genre_repository(genre_terror) -> DjangoORMGenreRepository:
    repository = DjangoORMGenreRepository()
    repository.save(genre_terror)
    return repository

@pytest.fixture
def video_repository() -> DjangoORMVideoRepository:
    return DjangoORMVideoRepository()


@pytest.mark.django_db
class TestCreateVideoWithoutMediaAPI:
    def test_create_with_success(
        self,
        castmember_repository: DjangoORMCastMemberRepository,
        genre_repository: DjangoORMGenreRepository ,
        category_repository: DjangoORMCategoryRepository,
        video_repository: DjangoORMVideoRepository
    ):

        url = "/api/video/video_without_media/"
        with freeze_time("2024-09-30 20:20:00"):
            response = APIClient().post(url, data={
                "title": "Filme teste",
                "description": "Testando cadastro",
                "duration": 250.5,
                "rating": "L",
                "launch_at": "2024-09-30",
                "categories": [category_repository.list()[0].id],
                "genres": [genre_repository.list()[0].id],
                "cast_members": [castmember_repository.list()[0].id]
            })

        assert response.status_code == status.HTTP_201_CREATED
        assert UUID(response.data['id'])
        video_raw = video_repository.list()
        assert len(video_raw) == 1
        video = video_raw[0]
        assert video.title == 'Filme teste'
        assert video.description == 'Testando cadastro'
        assert video.duration == 250.5
        assert video.rating == "L"
        assert str(video.launch_at) == "2024-09-30"
        assert video.categories == set([category_repository.list()[0].id])
        assert video.genres == set([genre_repository.list()[0].id])
        assert video.cast_members == set([castmember_repository.list()[0].id])
        assert video.updated_date is None
        assert str(video.created_date) == "2024-09-30 20:20:00+00:00"
    
    def test_create_with_invalid_name(
        self,
        castmember_repository: DjangoORMCastMemberRepository,
        genre_repository: DjangoORMGenreRepository ,
        category_repository: DjangoORMCategoryRepository,
    ):
        
        url = "/api/video/video_without_media/"
        response = APIClient().post(url, data={
            "title": "a"*300,
            "description": "Testando cadastro",
            "duration": 250.5,
            "rating": "L",
            "launch_at": "2024-09-30",
            "categories": [category_repository.list()[0].id],
            "genres": [genre_repository.list()[0].id],
            "cast_members": [castmember_repository.list()[0].id]
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'title' in response.data
        assert response.data['title'][0].code == 'max_length'

    def test_create_with_invalid_description(
        self,
        castmember_repository: DjangoORMCastMemberRepository,
        genre_repository: DjangoORMGenreRepository ,
        category_repository: DjangoORMCategoryRepository,
    ):
        
        url = "/api/video/video_without_media/"
        response = APIClient().post(url, data={
            "title": "Filme muitho loco",
            "description": "Testando cadastro"*2500,
            "duration": 250.5,
            "rating": "L",
            "launch_at": "2024-09-30",
            "categories": [category_repository.list()[0].id],
            "genres": [genre_repository.list()[0].id],
            "cast_members": [castmember_repository.list()[0].id]
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'description' in response.data
        assert response.data['description'][0].code == 'max_length'

    def test_create_with_invalid_duration(
        self,
        castmember_repository: DjangoORMCastMemberRepository,
        genre_repository: DjangoORMGenreRepository ,
        category_repository: DjangoORMCategoryRepository,
    ):
        
        url = "/api/video/video_without_media/"
        response = APIClient().post(url, data={
            "title": "Filme muitho loco",
            "description": "Testando cadastro",
            "duration": "asdasdas",
            "rating": "L",
            "launch_at": "2024-09-30",
            "categories": [category_repository.list()[0].id],
            "genres": [genre_repository.list()[0].id],
            "cast_members": [castmember_repository.list()[0].id]
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'duration' in response.data
        assert response.data['duration'][0].code == 'invalid'
    
    def test_create_with_invalid_negative_duration(
        self,
        castmember_repository: DjangoORMCastMemberRepository,
        genre_repository: DjangoORMGenreRepository ,
        category_repository: DjangoORMCategoryRepository,
    ):
        
        url = "/api/video/video_without_media/"
        response = APIClient().post(url, data={
            "title": "Filme muitho loco",
            "description": "Testando cadastro",
            "duration": -10,
            "rating": "L",
            "launch_at": "2024-09-30",
            "categories": [category_repository.list()[0].id],
            "genres": [genre_repository.list()[0].id],
            "cast_members": [castmember_repository.list()[0].id]
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
        assert response.data['error'] == 'Duration must greater then zero'

    def test_create_with_invalid_rating(
        self,
        castmember_repository: DjangoORMCastMemberRepository,
        genre_repository: DjangoORMGenreRepository ,
        category_repository: DjangoORMCategoryRepository,
    ):
        
        url = "/api/video/video_without_media/"
        response = APIClient().post(url, data={
            "title": "Filme muitho loco",
            "description": "Testando cadastro",
            "duration": 250,
            "rating": "Vintage",
            "launch_at": "2024-09-30",
            "categories": [category_repository.list()[0].id],
            "genres": [genre_repository.list()[0].id],
            "cast_members": [castmember_repository.list()[0].id]
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'rating' in response.data
        assert response.data['rating'][0].code == 'invalid_choice'

    def test_create_with_invalid_launch_date(
        self,
        castmember_repository: DjangoORMCastMemberRepository,
        genre_repository: DjangoORMGenreRepository ,
        category_repository: DjangoORMCategoryRepository,
    ):
        
        url = "/api/video/video_without_media/"
        response = APIClient().post(url, data={
            "title": "Filme muitho loco",
            "description": "Testando cadastro",
            "duration": 250,
            "rating": "L",
            "launch_at": "blabla",
            "categories": [category_repository.list()[0].id],
            "genres": [genre_repository.list()[0].id],
            "cast_members": [castmember_repository.list()[0].id]
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'launch_at' in response.data
        assert response.data['launch_at'][0].code == 'invalid'

    def test_create_with_invalid_entities(
        self,
        castmember_repository: DjangoORMCastMemberRepository,
        genre_repository: DjangoORMGenreRepository ,
        category_repository: DjangoORMCategoryRepository,
    ):
        
        url = "/api/video/video_without_media/"
        response = APIClient().post(url, data={
            "title": "Filme muitho loco",
            "description": "Testando cadastro",
            "duration": 250,
            "rating": "L",
            "launch_at": "2024-09-30",
            "categories": "asdasd",
            "genres": [genre_repository.list()[0].id],
            "cast_members": [castmember_repository.list()[0].id]
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'categories' in response.data
        assert response.data['categories'][0][0] == 'Must be a valid UUID.'

    def test_create_with_not_existing_entities(
        self,
        castmember_repository: DjangoORMCastMemberRepository,
        genre_repository: DjangoORMGenreRepository ,
        category_repository: DjangoORMCategoryRepository,
    ):
        
        url = "/api/video/video_without_media/"
        response = APIClient().post(url, data={
            "title": "Filme muitho loco",
            "description": "Testando cadastro",
            "duration": 250,
            "rating": "L",
            "launch_at": "2024-09-30",
            "categories": [uuid.uuid4()],
            "genres": [genre_repository.list()[0].id],
            "cast_members": [castmember_repository.list()[0].id]
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
        assert 'Categories ID not found' in response.data['error'] 
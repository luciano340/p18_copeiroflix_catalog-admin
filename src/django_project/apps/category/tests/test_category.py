from unicodedata import category
import uuid
from rest_framework.test import APIClient
import pytest
from rest_framework import status
from django_project.apps.category.repository import DjangoORMCategoryRepository
from src.core.category.domain.category import Category

@pytest.fixture
def category_movie():
    return  Category(
        name="Movie",
        description="Movie description",
    )

@pytest.fixture
def category_documentary():
    return Category(
        name="Documentary",
        description="Documentary description",
    )

@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()

@pytest.mark.django_db
class TestListAPI:


    def test_list_categories(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)

        url = '/api/categories/'
        response = APIClient().get(url)
        
        expected_data = {
            "data": [
                {
                    "id": str(category_movie.id),
                    "name": category_movie.name,
                    "description": category_movie.description,
                    "is_active": category_movie.is_active,
                    "created_date": category_movie.created_date,
                    "updated_date": category_movie.updated_date
                },
                {
                    "id": str(category_documentary.id),
                    "name": category_documentary.name,
                    "description": category_documentary.description,
                    "is_active": category_documentary.is_active,
                    "created_date": category_documentary.created_date,
                    "updated_date": category_documentary.updated_date
                }
            ]
        }     

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 2
        assert response.data == expected_data

@pytest.mark.django_db
class TestGetCategory:
    def test_return_error_when_id_is_invalid(self) -> None:
        url = '/api/categories/1231231231/'
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_return_category_when_exist(
            self,
            category_movie: Category,
            category_documentary: Category,
            category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)

        url = f'/api/categories/{category_documentary.id}/'
        response = APIClient().get(url)

        expected_data = {
            "data": {
                "id": str(category_documentary.id),
                "name": category_documentary.name,
                "description": category_documentary.description,
                "is_active": category_documentary.is_active,
                "created_date": category_documentary.created_date,
                "updated_date": category_documentary.updated_date
            }
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data
    
    def test_return_category_when_not_exist(self):
        url = f'/api/categories/{uuid.uuid4()}/'
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestCreateCategory:
    def test_when_payload_is_invalid_then_return_400(self) -> None:
        url = '/api/categories/'
        response = APIClient().post(
            url,
            data={
                "name": "",
                "description": "Filmes"
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_when_payload_is_valid_then_return_201(
        self,
        category_repository: DjangoORMCategoryRepository
    ) -> None:
        url = "/api/categories/"
        response = APIClient().post(
            url,
            data={
                "name": "Filme",
                "description": "Teste"
            }
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert category_repository.list() == [
            Category(
                id=uuid.UUID(response.data["id"]),
                name="Filme",
                description="Teste"
            )
        ]

@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_payload_is_invalid(self) -> None:
        url = "/api/categories/8383783749/"
        response = APIClient().put(
            url,
            data={
                "name": "",
                "description": "oi"
            },
            format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_when_payload_is_valid(
            self, 
            category_repository: DjangoORMCategoryRepository,
            category_documentary: Category
        ) -> None:

        category_repository.save(category_documentary)

        url = f"/api/categories/{category_documentary.id}/"
        response = APIClient().put(
            url,
            data={
                "name": "Luciano",
                "description": "oi",
                "is_active": "False"
            },
            format="json"
        )

        print(response.data)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_when_category_does_not_exist(self):
        url = f"/api/categories/{uuid.uuid4()}/"

        response = APIClient().put(
            url,
            data={
                "name": "Luciano",
                "description": "oi",
                "is_active": "False"
            },
            format="json"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
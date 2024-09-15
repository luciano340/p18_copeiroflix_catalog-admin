from datetime import datetime, timezone
import uuid
from rest_framework.test import APIClient
import pytest
from rest_framework import status
from src.django_project.apps.category.repository import DjangoORMCategoryRepository
from freezegun import freeze_time
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
                    "id": str(category_documentary.id),
                    "name": category_documentary.name,
                    "description": category_documentary.description,
                    "is_active": category_documentary.is_active,
                    "created_date": category_documentary.created_date,
                    "updated_date": category_documentary.updated_date
                },
                {
                    "id": str(category_movie.id),
                    "name": category_movie.name,
                    "description": category_movie.description,
                    "is_active": category_movie.is_active,
                    "created_date": category_movie.created_date,
                    "updated_date": category_movie.updated_date
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

        with freeze_time("2024-09-09 08:08:08"):
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
                description="Teste",
                created_date=datetime.fromisoformat("2024-09-09 08:08:08+00:00")
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

@pytest.mark.django_db
class TestDeleteAPI:
    def test_when_id_is_invalid(self):
        url = "/api/categories/8383783749/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_when_category_does_not_exist(self):
        url = f"/api/categories/{uuid.uuid4()}/"

        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_when_category_exit_then_delete(
            self,
            category_movie: Category,
            category_repository: DjangoORMCategoryRepository
    ) -> None:
        category_repository.save(category_movie)

        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert category_repository.list() == []

@pytest.mark.django_db
class TestUpdatePartialAPI:
    def test_when_payload_is_invalid(self) -> None:
        url = f"/api/categories/{uuid.uuid4()}/"
        response = APIClient().patch(
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
        with freeze_time("2024-09-01 03:03:03"):
            response = APIClient().patch(
                url,
                data={
                    "description": "oi",
                },
                format="json"
            )

        edited_category = category_repository.list()[0]

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert edited_category == Category(
            id=category_documentary.id,
            name=category_documentary.name,
            description="oi",
            is_active=category_documentary.is_active,
            created_date=datetime.fromisoformat(category_documentary.created_date).replace(tzinfo=timezone.utc),
            updated_date=datetime.fromisoformat("2024-09-01 03:03:03+00:00")
        )


    def test_when_category_does_not_exist(self):
        url = f"/api/categories/{uuid.uuid4()}/"

        response = APIClient().patch(
            url,
            data={
                "name": "Luciano",
                "description": "oi",
                "is_active": "False"
            },
            format="json"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
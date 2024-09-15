import pytest
from rest_framework.test import APIClient
from rest_framework import status
from freezegun import freeze_time

@freeze_time("2024-08-30 06:06:06")
@pytest.mark.django_db
class Teste2e:
    def test_user_can_do_anything_with_api(self) -> None:
        from src.core.category.domain.category import Category #Para que o freeze_time funciona no data de criação é necessário importar aqui, depois de definirmos o data freeze
        api_client = APIClient()

        list_response = api_client.get("/api/categories/")
        assert list_response.data == {
            "data": [],
            "meta": {
                "current_page": 1,
                "page_size": 5,
                "total": 0
            }
        }

        create_response = api_client.post(
            "/api/categories/",
            {
                "name": "Filme",
                "description": "Filmes muito loucos",
            },
            format="json"
        )

        assert create_response.status_code == status.HTTP_201_CREATED

        list_response = api_client.get("/api/categories/")
        assert list_response.status_code == status.HTTP_200_OK
        assert len(list_response.data["data"]) == 1
        assert list_response.data["meta"]["total"] == 1
        
        category_test = list_response.data["data"][0]

        with freeze_time("2024-09-01 03:03:03"):
            edit_response = api_client.put(
                f"/api/categories/{category_test['id']}/",
                data={
                    "name": "Serie",
                    "description": "Series em serie kkkk",
                    "is_active": "False"
                },
                format="json"
            )

        assert edit_response.status_code == status.HTTP_204_NO_CONTENT

        get_response = api_client.get(f"/api/categories/{category_test['id']}/")
        assert get_response.status_code == status.HTTP_200_OK
        
        category_test = get_response.data["data"]
        assert category_test == {
            "id": category_test['id'],
            "name": "Serie",
            "description": "Series em serie kkkk",
            "is_active": False,
            "created_date": "2024-08-30 06:06:06",
            "updated_date": "2024-09-01 03:03:03"
        }

        delete_response = api_client.delete(f"/api/categories/{category_test['id']}/")

        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

        list_response = api_client.get("/api/categories/")
        assert list_response.data == {
            "data": [],
            "meta": {
                "current_page": 1,
                "page_size": 5,
                "total": 0
            }
        }
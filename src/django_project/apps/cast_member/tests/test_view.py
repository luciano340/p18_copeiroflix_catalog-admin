from datetime import datetime
import uuid
from rest_framework.test import APIClient
import pytest
from rest_framework import status
from freezegun import freeze_time

from src.core.cast_member.domain.cast_member import CastMember
from src.django_project.apps.cast_member.repository import DjangoORMCastMemberRepository

@pytest.fixture
def CastMember_1():
    return  CastMember(
        name="Roberta",
        type="CONVIDADO",
    )

@pytest.fixture
def CastMember_2():
    return CastMember(
        name="Julio",
        type="APRESENTADOR",
    )

@pytest.fixture
def CastMember_repository() -> DjangoORMCastMemberRepository:
    return DjangoORMCastMemberRepository()


@pytest.mark.django_db
class TestListAPI:


    def test_list_categories(
        self,
        CastMember_1: CastMember,
        CastMember_2: CastMember,
        CastMember_repository: DjangoORMCastMemberRepository,
    ) -> None:
        CastMember_repository.save(CastMember_1)
        CastMember_repository.save(CastMember_2)

        url = '/api/cast_members/'
        response = APIClient().get(url)
        
        expected_data = {
            "data": [
                {
                    "id": str(CastMember_2.id),
                    "name": CastMember_2.name,
                    "type": CastMember_2.type,
                    "created_date": CastMember_2.created_date,
                    "updated_date": CastMember_2.updated_date
                },
                {
                    "id": str(CastMember_1.id),
                    "name": CastMember_1.name,
                    "type": CastMember_1.type,
                    "created_date": CastMember_1.created_date,
                    "updated_date": CastMember_1.updated_date
                }
            ],
            "meta": {
                "current_page": 1,
                "page_size": 5,
                "total": 2
            }
        }     

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 2
        assert response.data == expected_data

@pytest.mark.django_db
class TestGetCastMember:
    def test_return_error_when_id_is_invalid(self) -> None:
        url = '/api/cast_members/1231231231/'
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_return_CastMember_when_exist(
            self,
            CastMember_1: CastMember,
            CastMember_2: CastMember,
            CastMember_repository: DjangoORMCastMemberRepository,
    ) -> None:
        CastMember_repository.save(CastMember_1)
        CastMember_repository.save(CastMember_2)

        url = f'/api/cast_members/{CastMember_2.id}/'
        response = APIClient().get(url)

        expected_data = {
            "data": {
                "id": str(CastMember_2.id),
                "name": CastMember_2.name,
                "type": CastMember_2.type,
                "created_date": CastMember_2.created_date,
                "updated_date": CastMember_2.updated_date
            }
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data
    
    def test_return_CastMember_when_not_exist(self):
        url = f'/api/cast_members/{uuid.uuid4()}/'
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestCreateCastMember:
    def test_when_payload_is_invalid_then_return_400(self) -> None:
        url = '/api/cast_members/'
        response = APIClient().post(
            url,
            data={
                "name": "",
                "type": "ASTRONAUTA"
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_when_payload_is_valid_then_return_201(
        self,
        CastMember_repository: DjangoORMCastMemberRepository
    ) -> None:
        url = "/api/cast_members/"

        with freeze_time("2024-09-14 04:04:04"):
            response = APIClient().post(
                url,
                data={
                    "name": "André",
                    "type": "APRESENTADOR"
                }
            )

        cm_raw = CastMember(
            id=uuid.UUID(response.data["id"]),
            name="André",
            type="APRESENTADOR",
            created_date=datetime.fromisoformat("2024-09-14 04:04:04+00:00")
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert CastMember_repository.list() == [
            cm_raw
        ]

@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_payload_is_invalid(self) -> None:
        url = "/api/cast_members/8383783749/"
        response = APIClient().put(
            url,
            data={
                "name": "",
                "type": "Repolho"
            },
            format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_when_payload_is_valid(
            self, 
            CastMember_repository: DjangoORMCastMemberRepository,
            CastMember_2: CastMember
        ) -> None:

        CastMember_repository.save(CastMember_2)

        url = f"/api/cast_members/{CastMember_2.id}/"
        response = APIClient().put(
            url,
            data={
                "name": "Roberto",
                "type": "CONVIDADO",
            },
            format="json"
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_when_CastMember_does_not_exist(self):
        url = f"/api/cast_members/{uuid.uuid4()}/"

        response = APIClient().put(
            url,
            data={
                "name": "Julio",
                "type": "CONVIDADO",
            },
            format="json"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestDeleteAPI:
    def test_when_id_is_invalid(self):
        url = "/api/cast_members/8383783749/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_when_CastMember_does_not_exist(self):
        url = f"/api/cast_members/{uuid.uuid4()}/"

        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_when_CastMember_exit_then_delete(
            self,
            CastMember_1: CastMember,
            CastMember_repository: DjangoORMCastMemberRepository
    ) -> None:
        CastMember_repository.save(CastMember_1)

        url = f"/api/cast_members/{CastMember_1.id}/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert CastMember_repository.list() == []

@pytest.mark.django_db
class TestUpdatePartialAPI:
    def test_when_payload_is_invalid(self) -> None:
        url = f"/api/cast_members/{uuid.uuid4()}/"
        response = APIClient().patch(
            url,
            data={
                "name": "",
                "type": "APRESENTADOR"
            },
            format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_when_payload_is_valid(
            self, 
            CastMember_repository: DjangoORMCastMemberRepository,
            CastMember_2: CastMember
        ) -> None:

        CastMember_repository.save(CastMember_2)

        url = f"/api/cast_members/{CastMember_2.id}/"
        with freeze_time("2024-09-01 03:03:03"):
            response = APIClient().patch(
                url,
                data={
                    "type": "CONVIDADO",
                },
                format="json"
            )

        edited_CastMember = CastMember_repository.list()[0]

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert edited_CastMember.id == CastMember_2.id
        assert edited_CastMember.name == CastMember_2.name
        assert edited_CastMember.type == "CONVIDADO"
        assert edited_CastMember.updated_date.isoformat(sep=" ", timespec="seconds") == "2024-09-01 03:03:03+00:00"


    def test_when_CastMember_does_not_exist(self):
        url = f"/api/cast_members/{uuid.uuid4()}/"

        response = APIClient().patch(
            url,
            data={
                "name": "Julio",
                "type": "CONVIDADO",
            },
            format="json"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
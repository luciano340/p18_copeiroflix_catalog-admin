from uuid import UUID
import uuid

from freezegun import freeze_time
import pytest

from src.core.cast_member.application.use_cases.exceptions import CastMemberNotFound
from src.core.cast_member.application.use_cases.get_caster_member import GetCastMember, GetCastMemberRequest, GetCastMemberResponse
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestGetCastMember:
    def test_return_response_with_CastMember_data(self):
        with freeze_time("2020-01-01 00:00:00"):
            c = CastMember(
                name="Cassio",
                type="CONVIDADO"        
            )

        repository = InMemoryCastMemberRepository(
            castmembers=[c]
        )

        use_case = GetCastMember(repository)

        request = GetCastMemberRequest(
            id=c.id
        )

        response = use_case.execute(request)

        assert isinstance(response.id, UUID)
        assert repository.castmembers[0].id == response.id
        assert response == GetCastMemberResponse(
            id=c.id,
            name="Cassio",
            type="CONVIDADO",
            created_date="2020-01-01 00:00:00",
            updated_date=c.updated_date
        )
    
    def test_when_CastMember_not_exists(self):
        with freeze_time("2020-02-02 00:00:00"):
            c = CastMember(
                name="Alex",
                type="CONVIDADO"        
            )
        repository = InMemoryCastMemberRepository(
            castmembers=[c]
        )

        use_case = GetCastMember(repository)

        request = GetCastMemberRequest(
            id=uuid.uuid4()
        )

        with pytest.raises(CastMemberNotFound) as exc:
            use_case.execute(request)
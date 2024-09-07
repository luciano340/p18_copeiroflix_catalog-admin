import uuid

import pytest
from src.core.cast_member.application.use_cases.exceptions import CastMemberNotFound
from src.core.cast_member.application.use_cases.update_cast_member import UpdateCastMember, UpdateCastMemberRequest
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestUpdateCastMember:
    def test_can_update_CastMember_name_and_description(self):
        cast_member = CastMember(
            name="Charlie",
            type="CONVIDADO"
        )
        repository = InMemoryCastMemberRepository()
        repository.save(cast_member)

        use_case = UpdateCastMember(repository=repository)
        request=UpdateCastMemberRequest(
            id=cast_member.id,
            name="Luke",
            type="APRESENTADOR"
        )
        use_case.execute(request)
        updated_CastMember = repository.get_by_id(id=cast_member.id)
        
        assert updated_CastMember.name == "Luke"
        assert updated_CastMember.type == "APRESENTADOR"

    def test_fail_update_if_CastMember_not_exist(self):
        cast_member = CastMember(
            name="Penny",
            type="CONVIDADO"
        )
        repository = InMemoryCastMemberRepository()
        repository.save(cast_member)

        use_case = UpdateCastMember(repository=repository)
        request=UpdateCastMemberRequest(
            id=uuid.uuid4(),
            name="Richard",
        )
        
        with pytest.raises(CastMemberNotFound) as exc:
            use_case.execute(request)

from src.core.cast_member.application.use_cases.delete_cast_member import DeleteCastMember, DeleteCastMemberRequest
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestGetCastMember:
    def test_delete_CastMember_from_repository(self):
        c = CastMember(
            name="Pedro",
            type="CONVIDADO",
        )

        repository = InMemoryCastMemberRepository(
            castmembers=[c]
        )

        use_case = DeleteCastMember(repository=repository)

        request = DeleteCastMemberRequest(
            id=c.id
        )

        assert repository.get_by_id(c.id) is not None
        response = use_case.execute(request)

        assert repository.get_by_id(c.id) is None
        assert response is None
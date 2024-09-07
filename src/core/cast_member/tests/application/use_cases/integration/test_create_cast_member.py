from uuid import UUID

from src.core.cast_member.application.use_cases.create_cast_member import CreateCastMember, CreateCastMemberRequest
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository



class TestCreateCastMember:
    def test_create_CastMember_with_valid_data(self):
        repository = InMemoryCastMemberRepository()
        use_case = CreateCastMember(repository)

        c = CreateCastMemberRequest(
            name="Marlon",
            type="APRESENTADOR"
        )

        response = use_case.execute(c)

        assert isinstance(response.id, UUID)
        assert len(repository.castmembers) == 1
        
        assert repository.castmembers[0].id == response.id
        assert repository.castmembers[0].name == "Marlon"
        assert repository.castmembers[0].type == "APRESENTADOR"
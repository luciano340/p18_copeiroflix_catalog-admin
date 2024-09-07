from unittest.mock import create_autospec

from freezegun import freeze_time

from src.core.cast_member.application.use_cases.get_caster_member import GetCastMember, GetCastMemberRequest, GetCastMemberResponse
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository_interface import CastMemberRepositoryInterface


class TestGetCastMember:
    def test_return_found_CastMember(self):
        with freeze_time("2010-07-07 20:20:20"):
            cast_member = CastMember(
                name="Larissa",
                type="APRESENTADOR"
            )

        mock_repository = create_autospec(CastMemberRepositoryInterface)
        mock_repository.get_by_id.return_value = cast_member
        use_case = GetCastMember(repository=mock_repository)

        request = GetCastMemberRequest(
            id=cast_member.id
        )

        response = use_case.execute(request)

        assert response == GetCastMemberResponse(
            id=cast_member.id,
            name="Larissa",
            type="APRESENTADOR",
            created_date="2010-07-07 20:20:20",
            updated_date=None
        )


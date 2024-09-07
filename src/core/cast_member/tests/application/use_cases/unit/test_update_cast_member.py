from unittest.mock import create_autospec
import uuid
import pytest

from src.core.cast_member.application.use_cases.update_cast_member import UpdateCastMember, UpdateCastMemberRequest
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository_interface import CastMemberRepositoryInterface



class TestUpdateCastMember:
    def test_update_CastMember_name(self):
        mock_CastMember = CastMember(
            name="Rafael",
            type="CONVIDADO",
        )
        mock_repository = create_autospec(CastMemberRepositoryInterface)
        mock_repository.get_by_id.return_value = mock_CastMember

        use_case = UpdateCastMember(repository=mock_repository)
        request = UpdateCastMemberRequest(
            id=mock_CastMember.id,
            name="Rapahael",
            type="APRESENTADOR"
        )

        use_case.execute(request)

        assert mock_CastMember.name == "Rapahael"
        assert mock_CastMember.type == "APRESENTADOR"
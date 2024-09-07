from pickletools import pyset
from unittest.mock import create_autospec
from uuid import uuid4
import pytest

from src.core.cast_member.application.use_cases.delete_cast_member import DeleteCastMember, DeleteCastMemberRequest
from src.core.cast_member.application.use_cases.exceptions import CastMemberNotFound
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository_interface import CastMemberRepositoryInterface


class TestDeleteCastMember:
    def test_delete_CastMember_from_repository(self):
        cast_member = CastMember(
            name="Alexo",
            type="CONVIDADO"
        )
        
        mock_repository = create_autospec(CastMemberRepositoryInterface)
        mock_repository.get_by_id.return_value = CastMember

        use_case = DeleteCastMember(mock_repository)
        request = DeleteCastMemberRequest(
            id=cast_member.id
        )
        use_case.execute(request)

        mock_repository.delete_by_id.assert_called_once_with(cast_member.id)

    def test_when_CastMember_not_found_raise_exception(self):
        mock_repository = create_autospec(CastMemberRepositoryInterface)
        mock_repository.get_by_id.return_value = None

        use_case = DeleteCastMember(mock_repository)

        request = DeleteCastMemberRequest(
            id=uuid4()
        )

        with pytest.raises(CastMemberNotFound):
            use_case.execute(request)

        mock_repository.delete_by_id.assert_not_called()
        assert mock_repository.delete_by_id.called is False

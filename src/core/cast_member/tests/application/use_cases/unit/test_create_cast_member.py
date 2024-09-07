from unittest.mock import MagicMock
from uuid import UUID
import pytest

from src.core.cast_member.application.use_cases.create_cast_member import CreateCastMember, CreateCastMemberRequest
from src.core.cast_member.application.use_cases.exceptions import InvalidCastMemberData
from src.core.cast_member.domain.cast_member_repository_interface import CastMemberRepositoryInterface

class TestCreateCastMember:
    def test_create_CastMember_with_valid_data(self):
        mock_repository = MagicMock(CastMemberRepositoryInterface)
        use_case = CreateCastMember(mock_repository)

        c = CreateCastMemberRequest(
            name="Roberto",
            type="CONVIDADO",
        )

        response = use_case.execute(c)

        assert isinstance(response.id, UUID)
        assert mock_repository.save.called is True
    
    def test_create_CastMember_with_invalid_data(self):
        mock_repository = MagicMock(CastMemberRepositoryInterface)
        use_case = CreateCastMember(mock_repository)
        
        with pytest.raises(InvalidCastMemberData):
            c = CreateCastMemberRequest(
                name="",
            )
            c_id = use_case.execute(c)

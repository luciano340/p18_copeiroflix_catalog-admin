from unittest.mock import create_autospec
import uuid

from src.core._shared.dto import ListOuputMeta
from src.core.cast_member.application.use_cases.list_cast_member import CastMemberOutput, ListCastMember, RequestListCastMember, ResponseListCastMember
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository_interface import CastMemberRepositoryInterface


class TestListCastMember:
    def test_when_no_categories_found_then_return_empty_list(self):
        mock_repository = create_autospec(CastMemberRepositoryInterface)
        mock_repository.list.return_value = []

        use_case = ListCastMember(repository=mock_repository)
        request = RequestListCastMember()
        response = use_case.execute(request=request)

        assert response == ResponseListCastMember(
            data=[],
            meta=ListOuputMeta(current_page=1, page_size=5, total=0)
        )


    def test_when_has_categories_return_list_of_categories(self):
        cast_member1 = CastMember(
            name="Ronaldo",
            type="CONVIDADO"
        )

        cast_member2 = CastMember(
            id=uuid.uuid4(),
            name="Robson",
            type="CONVIDADO",
        )


        mock_repository = create_autospec(CastMemberRepositoryInterface)
        mock_repository.list.return_value = [
            cast_member1,
            cast_member2
        ]

        use_case = ListCastMember(repository=mock_repository)
        request = RequestListCastMember()
        response = use_case.execute(request=request)

        assert response == ResponseListCastMember(
            data=[
                CastMemberOutput(
                    id=cast_member1.id,
                    name="Ronaldo",
                    type="CONVIDADO",
                    created_date=cast_member1.created_date,
                    updated_date=cast_member1.updated_date
                ),
                CastMemberOutput(
                    id=cast_member2.id,
                    name="Robson",
                    type="CONVIDADO",
                    created_date=cast_member2.created_date,
                    updated_date=cast_member2.updated_date
                )
            ],
            meta=ListOuputMeta(current_page=1, page_size=5, total=2)
        )

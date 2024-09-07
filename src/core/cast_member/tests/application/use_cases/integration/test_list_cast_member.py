


from src.core.cast_member.application.use_cases.list_cast_member import CastMemberOutput, ListCastMember, RequestListCastMember, ResponseListCastMember
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestListCastMember:
    def test_return_empty(self):
        repository = InMemoryCastMemberRepository()

        use_case = ListCastMember(repository=repository)
        request = RequestListCastMember()
        response = use_case.execute(request=request)

        assert response == ResponseListCastMember(
            data=[]
        )


    def test_when_has_categories_return_list_of_categories(self):
        CastMember_1 = CastMember(
            name="Fernando",
            type="APRESENTADOR"
        )

        CastMember_2 = CastMember(
            name="Francisco",
            type="CONVIDADO",
        )


        repository = InMemoryCastMemberRepository()
        repository.save(CastMember_1)
        repository.save(CastMember_2)

        use_case = ListCastMember(repository=repository)
        request = RequestListCastMember()
        response = use_case.execute(request=request)

        assert response == ResponseListCastMember(
            data=[
                CastMemberOutput(
                    id=CastMember_1.id,
                    name="Fernando",
                    type="APRESENTADOR",
                    created_date=CastMember_1.created_date,
                    updated_date=CastMember_1.updated_date
                ),
                CastMemberOutput(
                    id=CastMember_2.id,
                    name="Francisco",
                    type="CONVIDADO",
                    created_date=CastMember_2.created_date,
                    updated_date=CastMember_2.updated_date
                )
            ]
        )

import pytest

from src.core.cast_member.domain.cast_member import CastMember
from src.django_project.apps.cast_member.models import CastMemberModel
from src.django_project.apps.cast_member.repository import DjangoORMCastMemberRepository


@pytest.mark.django_db
class TestRepository:
    def test_save_CastMember_in_database(self):
        cast_member = CastMember(
            name="Vicinicius",
            type="CONVIDADO"
        )

        repository = DjangoORMCastMemberRepository()

        assert CastMemberModel.objects.count() == 0
        repository.save(cast_member)
        assert CastMemberModel.objects.count() == 1
import pytest

from src.core.cast_member.domain.cast_member import CastMember
from src.django_project.apps.cast_member.models import CastMemberModel
from src.django_project.apps.cast_member.repository import DjangoORMCastMemberRepository


@pytest.mark.django_db
class TestRepository:
    def test_save_CastMember_in_database(self):
        cast_member = CastMember(
            name="Documentário",
            description="Chatão",
            is_active=False
        )

        repository = DjangoORMCastMemberRepository()

        assert CastMemberModel.objects.count() == 0
        repository.save(CastMember)
        assert CastMemberModel.objects.count() == 1
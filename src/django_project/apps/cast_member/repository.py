

from uuid import UUID
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository_interface import CastMemberRepositoryInterface
from src.django_project.apps.cast_member.models import CastMemberModel


class DjangoORMCastMemberRepository(CastMemberRepositoryInterface):
    def __init__(self, CastMember_model: CastMemberModel = CastMemberModel) -> None:
        self.CastMember_model = CastMember_model
    
    def save(self, cast_member: CastMember) -> None:
        self.CastMember_model.objects.create(
            id=cast_member.id,
            name=cast_member.name,
            type=cast_member.type,
            created_date=cast_member.created_date
        )
    
    def get_by_id(self, id: UUID) -> CastMember | None:
        try:
            cast_member_orm = self.CastMember_model.objects.get(id=id)
            return CastMember(
                id=cast_member_orm.id,
                name=cast_member_orm.name,
                type=cast_member_orm.type,
                created_date=cast_member_orm.created_date,
                updated_date=cast_member_orm.updated_date
            )
        except self.CastMember_model.DoesNotExist:
            return None
    
    def delete_by_id(self, id: UUID) -> None:
        self.CastMember_model.objects.filter(id=id).delete()
    
    def list(self) -> list[CastMember]:
        return [
            CastMember(
                id=cm.id,
                name=cm.name,
                type=cm.type,
                created_date=cm.created_date,
                updated_date=cm.updated_date
            )
            for cm in self.CastMember_model.objects.all()
        ]

    def update(self, castmember: CastMember) -> None:
        self.CastMember_model.objects.filter(pk=castmember.id).update(
            name=castmember.name,
            type=castmember.type,
            updated_date=castmember.updated_date
        )
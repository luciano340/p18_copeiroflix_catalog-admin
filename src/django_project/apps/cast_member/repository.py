

from uuid import UUID
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository_interface import CastMemberRepositoryInterface
from src.django_project.apps.cast_member.models import CastMemberModel


class DjangoORMCastMemberRepository(CastMemberRepositoryInterface):
    def __init__(self, CastMember_model: CastMemberModel = CastMemberModel) -> None:
        self.CastMember_model = CastMember_model
    
    def save(self, cast_member: CastMember) -> None:
        cast_member_model = CastMemberModelMapper.to_model(cast_member)
        cast_member_model.save()
    
    def get_by_id(self, id: UUID) -> CastMember | None:
        try:
            cast_member_orm = self.CastMember_model.objects.get(id=id)
            return CastMemberModelMapper.to_entity(cast_member_orm)
        except self.CastMember_model.DoesNotExist:
            return None
    
    def delete_by_id(self, id: UUID) -> None:
        self.CastMember_model.objects.filter(id=id).delete()
    
    def list(self, order_by: str = "name") -> list[CastMember]:
        return [
            CastMemberModelMapper.to_entity(cm)
            for cm in self.CastMember_model.objects.all().order_by(order_by)
        ]

    def update(self, castmember: CastMember) -> None:
        self.CastMember_model.objects.filter(pk=castmember.id).update(
            name=castmember.name,
            type=castmember.type,
            updated_date=castmember.updated_date
        )

class CastMemberModelMapper:
    @staticmethod
    def to_model(cast_member: CastMember) -> CastMemberModel:
        return CastMemberModel(
            id=cast_member.id,
            name=cast_member.name,
            type=cast_member.type,
            created_date=cast_member.created_date,
            updated_date=cast_member.updated_date
        )

    @staticmethod
    def to_entity(cast_member_model: CastMemberModel) -> CastMember:
        return CastMember(
            id=cast_member_model.id,
            name=cast_member_model.name,
            type=cast_member_model.type,
            created_date=cast_member_model.created_date,
            updated_date=cast_member_model.updated_date
        )
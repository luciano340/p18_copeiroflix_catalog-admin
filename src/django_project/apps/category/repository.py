from uuid import UUID
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository_interface import CategoryRepositoryInterface
from django_project.apps.category.models import Category as CategoryModel

class DjangoORMCategoryRepository(CategoryRepositoryInterface):
    def __init__(self, category_model: CategoryModel = CategoryModel) -> None:
        self.category_model = category_model
    
    def save(self, category: Category) -> None:
        self.category_model.objects.create(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
            created_date=category.created_date
        )
    
    def get_by_id(self, id: UUID) -> Category | None:
        try:
            category_orm = self.category_model.objects.get(id=id)
            return Category(
                id=category_orm.id,
                name=category_orm.name,
                description=category_orm.description,
                is_active=category_orm.is_active,
                created_date=category_orm.created_date,
                updated_date=category_orm.updated_date
            )
        except self.category_model.DoesNotExist:
            return None
    
    def delete_by_id(self, id: UUID) -> None:
        self.category_model.objects.filter(id=id).delete()
    
    def list(self) -> list[Category]:
        return [
            Category(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active,
                created_date=category.created_date,
                updated_date=category.updated_date
            )
            for category in self.category_model.objects.all()
        ]

    def update(self, category: Category) -> None:
        self.category_model.objects.filter(pk=category.id).update(
            name=category.name,
            description=category.description,
            is_active=category.is_active,
            updated_date=category.updated_date
        )
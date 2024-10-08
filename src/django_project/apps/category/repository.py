from uuid import UUID
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository_interface import CategoryRepositoryInterface
from src.django_project.apps.category.models import Category as CategoryModel

class DjangoORMCategoryRepository(CategoryRepositoryInterface):
    def __init__(self, category_model: CategoryModel = CategoryModel) -> None:
        self.category_model = category_model
    
    def save(self, category: Category) -> None:
        category_orm = CategoryModelMapper.to_model(category)
        category_orm.save()
    
    def get_by_id(self, id: UUID) -> Category | None:
        try:
            category_orm = self.category_model.objects.get(id=id)
            return CategoryModelMapper.to_entity(category_orm)
        except self.category_model.DoesNotExist:
            return None
    
    def delete_by_id(self, id: UUID) -> None:
        self.category_model.objects.filter(id=id).delete()
    
    def list(self, order_by: str = "name") -> list[Category]:
        return [
            CategoryModelMapper.to_entity(category_model)
            for category_model in self.category_model.objects.all().order_by(order_by)
        ]

    def update(self, category: Category) -> None:
        self.category_model.objects.filter(pk=category.id).update(
            name=category.name,
            description=category.description,
            is_active=category.is_active,
            updated_date=category.updated_date
        )

class CategoryModelMapper:
    @staticmethod
    def to_model(category: Category) -> CategoryModel:
        return CategoryModel(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
            created_date=category.created_date,
            updated_date=category.updated_date
        )

    @staticmethod
    def to_entity(category: CategoryModel) -> Category:
        return Category(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
            created_date=category.created_date,
            updated_date=category.updated_date
        )
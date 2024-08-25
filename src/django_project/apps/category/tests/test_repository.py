import pytest
from src.core.category.domain.category import Category
from django_project.apps.category.repository import DjangoORMCategoryRepository
from django_project.apps.category.models import Category as CategoryModel

@pytest.mark.django_db
class TestRepository:
    def test_save_category_in_database(self):
        category = Category(
            name="Documentário",
            description="Chatão",
            is_active=False
        )

        repository = DjangoORMCategoryRepository()

        assert CategoryModel.objects.count() == 0
        repository.save(category)
        assert CategoryModel.objects.count() == 1
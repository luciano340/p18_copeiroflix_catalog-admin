from uuid import UUID
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestInMemoryCategory:
    def test_can_save_category(self):
        repository = InMemoryCategoryRepository()
        category = Category(
            name="Filme",
            description="Teste"
        )

        repository.save(category)

        assert len(repository.categories) == 1
        assert repository.categories[0] == category
    
    def test_can_get_category(self):
        category = Category(
            name="Filme",
            description="Categoria de filme"
        )

        category2 = Category(
            name="Serie",
            description="Categoria de Serie",
            is_active=False
        )

        repository = InMemoryCategoryRepository(categories=[category, category2])
        response = repository.get_by_id(category.id)

        assert isinstance(response.id, UUID)
        assert response.id == category.id
        assert response.name == category.name
        assert response.description == category.description
        assert response.is_active == category.is_active

        assert response.id != category2.id
        assert response.name != category2.name
        assert response.description != category2.description
        assert response.is_active != category2.is_active


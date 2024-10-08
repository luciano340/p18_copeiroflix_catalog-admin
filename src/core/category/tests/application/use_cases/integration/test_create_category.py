from uuid import UUID
from src.core.category.application.use_cases.create_category import CreateCategory, CreateCategoryRequest
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(repository)

        c = CreateCategoryRequest(
            name="Filme",
            description="Categoria Filme",
            is_active=True
        )

        response = use_case.execute(c)

        assert isinstance(response.id, UUID)
        assert len(repository.categories) == 1
        
        assert repository.categories[0].id == response.id
        assert repository.categories[0].name == "Filme"
        assert repository.categories[0].description == "Categoria Filme"
        assert repository.categories[0].is_active is True
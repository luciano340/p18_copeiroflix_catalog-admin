from os import name
from unicodedata import category
from urllib import request
import uuid
import pytest
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestUpdateCategory:
    def test_can_update_category_name_and_description(self):
        category = Category(
            name="Filme",
            description="Teste"
        )
        repository = InMemoryCategoryRepository()
        repository.save(category)

        use_case = UpdateCategory(repository=repository)
        request=UpdateCategoryRequest(
            id=category.id,
            name="Luke",
            description="O gato"
        )
        use_case.execute(request)
        updated_category = repository.get_by_id(id=category.id)
        
        assert updated_category.name == "Luke"
        assert updated_category.description == "O gato"
    
    def test_can_update_category_status(self):
        category = Category(
            name="Filme",
            description="Teste"
        )
        repository = InMemoryCategoryRepository()
        repository.save(category)

        use_case = UpdateCategory(repository=repository)
        request=UpdateCategoryRequest(
            id=category.id,
            name="Luke",
            description="O gato",
            is_active=False
        )
        use_case.execute(request)
        updated_category = repository.get_by_id(id=category.id)
        
        assert updated_category.name == "Luke"
        assert updated_category.description == "O gato"
        assert updated_category.is_active is False

    def test_fail_update_if_category_not_exist(self):
        category = Category(
            name="Filme",
            description="Teste"
        )
        repository = InMemoryCategoryRepository()
        repository.save(category)

        use_case = UpdateCategory(repository=repository)
        request=UpdateCategoryRequest(
            id=uuid.uuid4(),
            name="Luke",
            description="O gato",
            is_active=False
        )
        
        with pytest.raises(CategoryNotFound, match=f"Category with id {request.id} not found") as exc:
            use_case.execute(request)
from uuid import UUID
import uuid

import pytest
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestGetCategory:
    def test_return_response_with_category_data(self):
        c = Category(
            name="Filme",
            description="Random",
            is_active=False
        )

        repository = InMemoryCategoryRepository(
            categories=[c]
        )

        use_case = GetCategory(repository)

        request = GetCategoryRequest(
            id=c.id
        )

        response = use_case.execute(request)

        assert isinstance(response.id, UUID)
        assert repository.categories[0].id == response.id
        assert response == GetCategoryResponse(
            id=c.id,
            name=c.name,
            description=c.description,
            is_active=c.is_active,
            created_date=c.created_date,
            updated_date=c.updated_date
        )
    
    def test_when_category_not_exists(self):
        c = Category(
            name="Filme",
            description="Random",
            is_active=False
        )

        repository = InMemoryCategoryRepository(
            categories=[c]
        )

        use_case = GetCategory(repository)

        request = GetCategoryRequest(
            id=uuid.uuid4()
        )

        with pytest.raises(CategoryNotFound) as exc:
            use_case.execute(request)
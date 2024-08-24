from uuid import UUID
import uuid

import pytest
from src.core.category.application.use_cases.delete_category import DeleteCategory, DeleteCategoryRequest
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestGetCategory:
    def test_delete_category_from_repository(self):
        c = Category(
            name="Filme",
            description="Random",
            is_active=False
        )

        repository = InMemoryCategoryRepository(
            categories=[c]
        )

        use_case = DeleteCategory(repository=repository)

        request = DeleteCategoryRequest(
            id=c.id
        )

        assert repository.get_by_id(c.id) is not None
        response = use_case.execute(request)

        assert repository.get_by_id(c.id) is None
        assert response is None
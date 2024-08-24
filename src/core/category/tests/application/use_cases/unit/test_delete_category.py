from pickletools import pyset
from unittest.mock import create_autospec
from uuid import uuid4

import pytest
from src.core.category.application.category_repository_interface import CategoryRepositoryInterface
from src.core.category.application.use_cases.delete_category import DeleteCategory, DeleteCategoryRequest
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.domain.category import Category


class TestDeleteCategory:
    def test_delete_category_from_repository(self):
        category = Category(
            name="Filme",
            description="Categoria filme"
        )
        mock_repository = create_autospec(CategoryRepositoryInterface)
        mock_repository.get_by_id.return_value = category

        use_case = DeleteCategory(mock_repository)
        request = DeleteCategoryRequest(
            id=category.id
        )
        use_case.execute(request)

        mock_repository.delete_by_id.assert_called_once_with(category.id)

    def test_when_category_not_found_raise_exception(self):
        mock_repository = create_autospec(CategoryRepositoryInterface)
        mock_repository.get_by_id.return_value = None

        use_case = DeleteCategory(mock_repository)

        request = DeleteCategoryRequest(
            id=uuid4()
        )

        with pytest.raises(CategoryNotFound):
            use_case.execute(request)

        mock_repository.delete_by_id.assert_not_called()
        assert mock_repository.delete_by_id.called is False

from unittest.mock import create_autospec
import uuid

import pytest
from src.core.category.domain.category_repository_interface import CategoryRepositoryInterface
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from src.core.category.domain.category import Category


class TestUpdateCategory:
    def test_update_category_name(self):
        mock_category = Category(
            name="Filme",
            description="Categoria Filme",
            is_active=False
        )
        mock_repository = create_autospec(CategoryRepositoryInterface)
        mock_repository.get_by_id.return_value = mock_category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(
            id=mock_category.id,
            name="Globo"
        )

        use_case.execute(request)

        assert mock_category.name == "Globo"
        assert mock_category.description == "Categoria Filme"

    def test_update_category_description(self):
        mock_category = Category(
            name="Filme",
            description="Categoria Filme",
            is_active=False
        )
        mock_repository = create_autospec(CategoryRepositoryInterface)
        mock_repository.get_by_id.return_value = mock_category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(
            id=mock_category.id,
            description="Atualizado"
        )
        
        use_case.execute(request)

        assert mock_category.name == "Filme"
        assert mock_category.description == "Atualizado"

    def test_can_deactivate_category(self):
        mock_category = Category(
            name="Filme",
            description="Categoria Filme",
            is_active=True
        )
        mock_repository = create_autospec(CategoryRepositoryInterface)
        mock_repository.get_by_id.return_value = mock_category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(
            id=mock_category.id,
            is_active=False
        )
        
        use_case.execute(request)

        assert mock_category.name == "Filme"
        assert mock_category.description == "Categoria Filme"
        assert mock_category.is_active is False

    def test_can_activate_category(self):
        mock_category = Category(
            name="Filme",
            description="Categoria Filme",
            is_active=False
        )
        mock_repository = create_autospec(CategoryRepositoryInterface)
        mock_repository.get_by_id.return_value = mock_category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(
            id=mock_category.id,
            is_active=True
        )
        
        use_case.execute(request)

        assert mock_category.name == "Filme"
        assert mock_category.description == "Categoria Filme"
        assert mock_category.is_active is True
    
    def test_fail_update_if_category_not_exist(self):
        mock_category = Category(
            name="Filme",
            description="Categoria Filme",
            is_active=False
        )
        mock_repository = create_autospec(CategoryRepositoryInterface)
        mock_repository.get_by_id.return_value = None

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(
            id=uuid.uuid4(),
            is_active=True
        )
        with pytest.raises(CategoryNotFound):
            use_case.execute(request)
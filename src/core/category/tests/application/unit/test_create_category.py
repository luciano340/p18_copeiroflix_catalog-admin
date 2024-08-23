from unittest.mock import MagicMock
from uuid import UUID
import pytest
from src.core.category.application.category_repository_interface import CategoryRepositoryInterface
from src.core.category.application.create_category import CreateCategory, CreateCategoryRequest, InvalidCategoryData

class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        mock_repository = MagicMock(CategoryRepositoryInterface)
        use_case = CreateCategory(mock_repository)

        c = CreateCategoryRequest(
            name="Filme",
            description="Categoria Filme",
            is_active=True
        )

        response = use_case.execute(c)

        assert isinstance(response.id, UUID)
        assert mock_repository.save.called is True
    
    def test_create_category_with_invalid_data(self):
        mock_repository = MagicMock(CategoryRepositoryInterface)
        use_case = CreateCategory(mock_repository)
        
        with pytest.raises(InvalidCategoryData):
            c = CreateCategoryRequest(
                name=""
            )
            c_id = use_case.execute(c)

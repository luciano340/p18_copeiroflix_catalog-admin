from unicodedata import category
from unittest.mock import create_autospec
import uuid
from src.core.category.application.category_repository_interface import CategoryRepositoryInterface
from src.core.category.application.use_cases.list_category import CategoryOutput, ListCategory, ListCategoryRequest, ListCategoryResponse
from src.core.category.domain.category import Category


class TestListCategory:
    def test_when_no_categories_found_then_return_empty_list(self):
        mock_repository = create_autospec(CategoryRepositoryInterface)
        mock_repository.list.return_value = []

        use_case = ListCategory(repository=mock_repository)
        request = ListCategoryRequest()
        response = use_case.execute(request=request)

        assert response == ListCategoryResponse(
            data=[]
        )


    def test_when_has_categories_return_list_of_categories(self):
        category_filme = Category(
            
            name="Filme",
            description="Filmes muito loucos"
        )

        category_serie = Category(
            id=uuid.uuid4(),
            name="Documentário",
            description="Documentários chatos",
            is_active=False
        )


        mock_repository = create_autospec(CategoryRepositoryInterface)
        mock_repository.list.return_value = [
            category_filme,
            category_serie
        ]

        use_case = ListCategory(repository=mock_repository)
        request = ListCategoryRequest()
        response = use_case.execute(request=request)

        assert response == ListCategoryResponse(
            data=[
                CategoryOutput(
                    id=category_filme.id,
                    name=category_filme.name,
                    description=category_filme.description,
                    is_active=category_filme.is_active
                ),
                CategoryOutput(
                    id=category_serie.id,
                    name=category_serie.name,
                    description=category_serie.description,
                    is_active=category_serie.is_active
                )
            ]
        )

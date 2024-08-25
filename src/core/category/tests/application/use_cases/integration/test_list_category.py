from unicodedata import category
from unittest.mock import create_autospec
import uuid
from src.core.category.domain.category_repository_interface import CategoryRepositoryInterface
from src.core.category.application.use_cases.list_category import CategoryOutput, ListCategory, ListCategoryRequest, ListCategoryResponse
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestListCategory:
    def test_return_empty(self):
        repository = InMemoryCategoryRepository()

        use_case = ListCategory(repository=repository)
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


        repository = InMemoryCategoryRepository()
        repository.save(category_filme)
        repository.save(category_serie)

        use_case = ListCategory(repository=repository)
        request = ListCategoryRequest()
        response = use_case.execute(request=request)

        assert response == ListCategoryResponse(
            data=[
                CategoryOutput(
                    id=category_filme.id,
                    name=category_filme.name,
                    description=category_filme.description,
                    is_active=category_filme.is_active,
                    created_date=category_filme.created_date,
                    updated_date=category_filme.updated_date
                ),
                CategoryOutput(
                    id=category_serie.id,
                    name=category_serie.name,
                    description=category_serie.description,
                    is_active=category_serie.is_active,
                    created_date=category_serie.created_date,
                    updated_date=category_serie.updated_date
                )
            ]
        )

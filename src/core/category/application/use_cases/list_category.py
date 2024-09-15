from dataclasses import dataclass, field
import os
from uuid import UUID
from datetime import datetime
from django.core.exceptions import FieldError
from src.core._shared.dto import ListOuputMeta
from src.core._shared.factory_pagination import CreateListPagination
from src.core.category.application.use_cases.exceptions import CategoryOrderNotFound
from src.core.category.domain.category_repository_interface import CategoryRepositoryInterface

@dataclass
class ListCategoryRequest:
    order_by: str = "name"
    current_page: int = 1

@dataclass
class CategoryOutput:
    id: UUID
    name: str
    description: str
    is_active: bool
    created_date: datetime
    updated_date: datetime

@dataclass
class ListCategoryResponse:
    data: list[CategoryOutput]
    meta: ListOuputMeta = field(default_factory=ListOuputMeta)


class ListCategory:
    def __init__(self, repository: CategoryRepositoryInterface) -> None:
        self.repository = repository
    
    def execute(self, request: ListCategoryRequest) -> ListCategoryResponse:
        try:
            categories = self.repository.list(order_by=request.order_by)
        except FieldError:
            raise CategoryOrderNotFound(f'Field {request.order_by} not found')
        
        categories = [
            CategoryOutput(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active,
                created_date=category.created_date,
                updated_date=category.updated_date
            ) for category in categories
        ]

        categories_page = CreateListPagination.configure_pagination(
            mapped_list=categories, 
            current_page=request.current_page
        )

        return ListCategoryResponse(
            data=categories_page,
            meta=ListOuputMeta(
                current_page=request.current_page,
                page_size=os.environ.get("page_size", 5),
                total=len(categories)
            )
        )
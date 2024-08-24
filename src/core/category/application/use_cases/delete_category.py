from dataclasses import dataclass
from uuid import UUID
from src.core.category.application.category_repository_interface import CategoryRepositoryInterface
from src.core.category.application.use_cases.exceptions import CategoryNotFound

@dataclass
class DeleteCategoryRequest:
    id: UUID


class DeleteCategory:
    def __init__(self, repository: CategoryRepositoryInterface) -> None:
        self.repository = repository
    
    def execute(self, request: DeleteCategoryRequest):
        category = self.repository.get_by_id(id=request.id)

        if category is None:
            raise CategoryNotFound(f"Category with id {request.id} not found for delete")
        
        self.repository.delete_by_id(id=request.id)


from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
import uuid

@dataclass
class Genre:
    name: str
    is_active: bool = True
    created_date: datetime = field(default_factory=lambda: datetime.now().isoformat(sep=" ", timespec="seconds"))
    updated_date: datetime = None
    id:  uuid.UUID = field(default_factory=uuid.uuid4)
    categories: set[UUID] = field(default_factory=set)

    def __post_init__(self):
        self.__validation()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Genre):
            return False
        
        return self.id == other.id

    def change_name(self, name: str = "") -> None:
        self.name = name
        self.updated_date = datetime.now().isoformat(sep=" ", timespec="seconds")
        self.__validation()
    
    def activate(self) -> None:
        self.is_active = True
        self.updated_date = datetime.now().isoformat(sep=" ", timespec="seconds")
        self.__validation()

    def deactivate(self) -> None:
        self.is_active = False
        self.updated_date = datetime.now().isoformat(sep=" ", timespec="seconds")
        self.__validation()

    def add_caterogy(self, category_id: UUID) -> None:
        self.categories.add(category_id)
        self.__validation()
    
    def remove_category(self, category_id: UUID) -> None:
        self.categories.remove(category_id)
        self.__validation()

    def __validation(self):
        if len(self.name) > 255:
            raise ValueError("name must have less than 255 characteres")
    
        if not self.name:
            raise ValueError("name cannot be empty")
    
        if len(self.categories) > 0:
            uuid_to_str = str(list(self.categories)[-1])
            try:
                UUID(uuid_to_str)
            except:
                raise ValueError(f"Not a valid UUID: {uuid_to_str}")
        
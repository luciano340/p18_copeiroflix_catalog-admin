from dataclasses import dataclass, field
from datetime import datetime

from src.core._shared.entity import Entity


@dataclass
class Category(Entity):
    name: str
    description: str = ""
    is_active: bool = True
    created_date: datetime = field(default_factory=lambda: datetime.now().isoformat(sep=" ", timespec="seconds"))
    updated_date: datetime = None
    
    def __post_init__(self):
        self.__validation()

    def __str__(self) -> str:
        return f"str {self.id} - {self.name} - {self.description} - {self.is_active} - {self.created_date} - {self.updated_date}"

    def __repr__(self) -> str:
        return f"repr {self.id} - {self.name} - {self.description} - {self.is_active}"
        
        return self.id == other.id

    def update_category(self, name: str = "", description: str = "") -> None:
        self.name = name
        self.description = description
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

    def __validation(self):
        if len(self.name) > 255:
            self.notificaiton.add_error("name must have less than 255 characteres")
    
        if not self.name:
            self.notificaiton.add_error("name cannot be empty")
        
        if self.notificaiton.has_errors:
            raise ValueError(self.notificaiton.messages)
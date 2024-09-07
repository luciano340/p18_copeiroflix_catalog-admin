from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
import uuid

class CastMemberType(StrEnum):
    CONVIDADO = "CONVIDADO"
    APRESENTADOR = "APRESENTADOR"

@dataclass
class CastMember:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_date: datetime = field(default_factory=lambda: datetime.now().isoformat(sep=" ", timespec="seconds"))
    updated_date: datetime = None
    name: str = None
    type: CastMemberType = None

    def __post_init__(self):
        self.__validation()

    def __str__(self) -> str:
        return f"str {self.id} - {self.name} - {self.type} - {self.created_date} - {self.updated_date}"

    def __repr__(self) -> str:
        return f"repr {self.id} - {self.name} - {self.type}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CastMember):
            return False
        return self.id == other.id

    def update_cast_member(self, name: str = "", type: CastMemberType = None) -> None:
        if name:
            self.name = name
        if type:
            self.type = type
        self.updated_date = datetime.now().isoformat(sep=" ", timespec="seconds")
        self.__validation()

    def __validation(self):
        if not self.name:
            raise ValueError("name cannot be empty")
        if len(self.name) > 255:
            raise ValueError("name must have less than 255 characters")
        if self.type not in CastMemberType:
            raise ValueError(f"type must be one of {list(CastMemberType)}")
        if not self.type:
            raise ValueError("type cannot be empty")
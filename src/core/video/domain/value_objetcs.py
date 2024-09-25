from dataclasses import dataclass
from enum import StrEnum, auto, unique
from uuid import UUID

@unique
class MediaStatus(StrEnum):
    PENDING = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    ERROR = auto()

@unique
class Rating(StrEnum):
    ER = auto()
    L = auto()
    AGE_10 = auto()
    AGE_12 = auto()
    AGE_14 = auto()
    AGE_16 = auto()
    AGE_18 = auto()

@dataclass(frozen=True)
class ImageMedia:
    id: UUID
    check_sum: str
    name: str
    location: str
    
@dataclass(frozen=True)
class AudioVideoMedia:
    id: UUID
    check_sum: str
    name: str
    raw_location: str
    encoded_locatiom: str
    status: MediaStatus
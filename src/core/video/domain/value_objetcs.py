from dataclasses import dataclass
from enum import StrEnum, auto, unique
from uuid import UUID

@unique
class MediaStatus(StrEnum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"

@unique
class Rating(StrEnum):
    ER = "ER"
    L = "L"
    AGE_10 = "AGE_10"
    AGE_12 = "AGE_12"
    AGE_14 = "AGE_14"
    AGE_16 = "AGE_16"
    AGE_18 = "AGE_18"

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
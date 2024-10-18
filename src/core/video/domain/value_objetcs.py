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
class AudioMediaType(StrEnum):
    VIDEO = "VIDEO"
    TRAILER = "TRAILER"

@unique
class ImageMediaType(StrEnum):
    THUMBNAIL_HALF = "THUMBNAIL_HALF"
    THUMBNAIL = "THUMBNAIL"
    BANNER = "BANNER"

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
    name: str
    location: str
    type: ImageMediaType

@dataclass(frozen=True)
class AudioVideoMedia:
    name: str
    raw_location: str
    encoded_location: str
    status: MediaStatus
    type: AudioMediaType
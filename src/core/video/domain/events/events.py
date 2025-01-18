from dataclasses import dataclass
from uuid import UUID

from src.core.video.domain.value_objetcs import AudioMediaType


@dataclass(frozen=True)
class AudioVideoMediaUpdated:
    aggregate_id: UUID
    file_path: str
    media_type: AudioMediaType
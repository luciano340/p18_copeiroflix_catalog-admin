from dataclasses import dataclass

from src.core._shared.events.event import Event
from src.core.video.domain.value_objetcs import AudioMediaType


@dataclass(frozen=True)
class AudioVideoMediaUpdatedIntegrationEvent(Event):
    resource_id: str
    file_path: str
    type: AudioMediaType
    
    def to_dict(self) -> dict:
        return {
            "resource_id": str(self.resource_id),
            "file_path": self.file_path,
            "media_type": self.type.value,
        }
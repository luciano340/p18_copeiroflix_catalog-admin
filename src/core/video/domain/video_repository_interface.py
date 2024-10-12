from abc import ABC, abstractmethod
from uuid import UUID

from src.core.video.domain.value_objetcs import AudioMediaType, ImageMedia, ImageMediaType
from src.core.video.domain.video import Video


class VideoRepositoryInterface(ABC):
    @abstractmethod
    def save(self, video: Video) -> Video:
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Video | None:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self,id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, video: Video) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def update_media(self, video: Video, video_type: AudioMediaType) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_image(self, video: Video, image_type: ImageMediaType) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(self, order_by: str = "title") -> list[Video]:
        raise NotImplementedError
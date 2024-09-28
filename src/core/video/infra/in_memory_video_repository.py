from uuid import UUID

from src.core.video.domain.video import Video
from src.core.video.domain.video_repository_interface import VideoRepositoryInterface


class InMemoryVideoRepository(VideoRepositoryInterface):
    def __init__(self, videos=None) -> None:
        self.videos = videos or []
    
    def save(self, video: Video) -> None:
        self.videos.append(video)
    
    def get_by_id(self, id: UUID) -> Video | None:
        for c in self.videos:
            if c.id == id:
                return c
        return None

    def delete_by_id(self, id: UUID) -> None:
        for n, i in enumerate(self.videos):
            if i.id == id:
                self.videos.pop(n)
    
    def update(self, genre: Video) -> None:
        for n, i in enumerate(self.videos):
            if i.id == genre.id:
                self.videos[n] = genre

    def list(self, order_by: str = "name") -> list[Video]:
        return [c for c in self.videos]
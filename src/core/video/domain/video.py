from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID


from src.core._shared.entity import Entity
from src.core.video.domain.value_objetcs import AudioVideoMedia, ImageMedia, Rating


@dataclass
class Video(Entity):
    title: str
    description: str
    duration: Decimal
    rating: Rating
    banner: ImageMedia | None = None
    thumbnail: ImageMedia | None = None
    thumbnail_half: ImageMedia | None = None
    trailer: AudioVideoMedia | None = None
    video: AudioVideoMedia | None = None
    categories: set[UUID] = field(default_factory=set)
    genres: set[UUID] = field(default_factory=set)
    cast_members: set[UUID] = field(default_factory=set)
    created_date: datetime = field(default_factory=lambda: datetime.now().isoformat(sep=" ", timespec="seconds"))
    updated_date: datetime = None
    launch_at: datetime = field(default_factory=lambda: datetime.now().isoformat(sep=" ", timespec="seconds"))
    published: bool = False

    def __post_init__(self):
        self.__validation()

    def __validation(self):
        if len(self.title) > 255:
            self.notificaiton.add_error("Title must have less than 255 characteres")
    
        if not self.title:
            self.notificaiton.add_error("Title cannot be empty")
        
        if self.duration <= 0:
            self.notificaiton.add_error("Duration must greater then zero")

        if len(self.categories) == 0:
            self.notificaiton.add_error("The movie must be at least one category")
        
        if len(self.genres) == 0:
            self.notificaiton.add_error("The movie must be at least one genre")
        
        if len(self.cast_members) == 0:
            self.notificaiton.add_error("The movie must be at least one cast_member")

        if self.launch_at == None:
            self.notificaiton.add_error("The date of launch cannot be null")

        if self.notificaiton.has_errors:
            raise ValueError(self.notificaiton.messages)
    
    def update(self, title: str = None, description: str = None, duration: Decimal = None, rating: Rating = None, published: bool = None, launch_at: datetime = None):
        for key, value in locals():
            if value == None:
                continue
            setattr(self, key, value)
        self.__validation()
    
    def add_category(self, category: UUID|list[UUID]) -> None:
        if isinstance(category, list):
            self.categories.update(category)
        else:
            self.categories.add(category)
        self.__validation()

    def add_genres(self, genre: UUID|list[UUID]) -> None:
        if isinstance(genre, list):
            self.genres.update(genre)
        else:
            self.genres.add(genre)
        self.__validation()

    def add_cast_member(self, cast_member: UUID|list[UUID]) -> None:
        if isinstance(cast_member, list):
            self.cast_members.update(cast_member)
        else:
            self.cast_members.add(cast_member)
        self.__validation()

    def update_banner(self, banner: ImageMedia) -> None:
        self.banner = banner
        self.__validation()

    def update_thumbnail(self, thumbnail: ImageMedia) -> None:
        self.thumbnail = thumbnail
        self.__validation()

    def update_thumbnail_half(self, thumbnail_half: ImageMedia) -> None:
        self.thumbnail_half = thumbnail_half
        self.__validation()

    def update_trailer(self, trailer: AudioVideoMedia) -> None:
        self.trailer = trailer
        self.__validation()

    def update_video(self, video: AudioVideoMedia) -> None:
        self.video = video
        self.__validation()
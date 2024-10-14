from datetime import datetime
import uuid
from django.db import models

from src.core.video.domain.value_objetcs import AudioMediaType, ImageMediaType, MediaStatus, Rating

class Video(models.Model):
    RATING_CHOICES = [(rating.name, rating.name) for rating in Rating]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    launch_at = models.DateField()
    duration = models.DecimalField(max_digits=10, decimal_places=2)
    published = models.BooleanField()
    rating = models.CharField(max_length=10, choices=RATING_CHOICES)
    categories = models.ManyToManyField('category.Category', related_name='videos')
    genres = models.ManyToManyField('genre.Genre', related_name='videos')
    cast_members = models.ManyToManyField('cast_member.CastMemberModel', related_name='videos')
    created_date = models.DateTimeField(default=datetime.now)
    updated_date = models.DateTimeField(default=None, null=True)
    banner = models.ForeignKey("ImageMedia", null=True, blank=True, related_name="banner", on_delete=models.SET_NULL)
    thumbnail = models.ForeignKey("ImageMedia", null=True, blank=True, related_name="video_thumbnail", on_delete=models.SET_NULL)
    thumbnail_half = models.ForeignKey("ImageMedia", null=True, blank=True, related_name="video_thumbnail_half", on_delete=models.SET_NULL)
    trailer = models.ForeignKey("AudioVideoMedia", null=True, blank=True, related_name="video_trailer", on_delete=models.SET_NULL)
    video = models.ForeignKey("AudioVideoMedia", null=True, blank=True, related_name="video_media", on_delete=models.SET_NULL)

    class Meta:
        db_table = "videos"

class ImageMedia(models.Model):
    IMAGE_TYPE_CHOICE = [(type.name, type.name) for type in ImageMediaType ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=1024)
    type = models.CharField(max_length=20, choices=IMAGE_TYPE_CHOICE)
    
    class Meta:
        db_table = "videos_imagemedia"

class AudioVideoMedia(models.Model):
    STATUS_CHOICE = [(status.name, status.name) for status in MediaStatus ]
    MEDIA_TYPE_CHOICE = [(type.name, type.name) for type in AudioMediaType ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    raw_location = models.CharField(max_length=1024)
    encoded_location = models.CharField(max_length=1024)
    status = models.CharField(max_length=20, choices=STATUS_CHOICE)
    type = models.CharField(max_length=20, choices=MEDIA_TYPE_CHOICE)
    
    class Meta:
        db_table = "videos_audiovideomedia"
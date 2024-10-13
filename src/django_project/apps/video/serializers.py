from email.policy import default
from rest_framework import serializers

from src.core.video.domain.value_objetcs import AudioMediaType, MediaStatus, Rating
from src.django_project.apps._shared.serializers import ListOutputMetaSerializer

class SetField(serializers.ListField):
    def to_internal_value(self, data):
        return set(super().to_internal_value(data))
    
    def to_representation(self, data):
        return list(super().to_representation(data))

class RatingTypeField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        choices = [(type.name, type.value) for type in Rating]
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        return Rating(super().to_internal_value(data))

    def to_representation(self, value):
        return str(super().to_representation(value))

class StatusTypeField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        choices = [(type.name, type.value) for type in MediaStatus]
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        return MediaStatus(super().to_internal_value(data))

    def to_representation(self, value):
        return str(super().to_representation(value))

class AudioMediaTypeField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        choices = [(type.name, type.value) for type in AudioMediaType]
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        return AudioMediaType(super().to_internal_value(data))

    def to_representation(self, value):
        return str(super().to_representation(value))

class ImageMediaTypeField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        choices = [(type.name, type.value) for type in AudioMediaType]
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        return AudioMediaType(super().to_internal_value(data))

    def to_representation(self, value):
        return str(super().to_representation(value))
    
class AudioVideoMediaOutput(serializers.Serializer):
    name = serializers.CharField(max_length=255, allow_blank=False)
    raw_location = serializers.CharField(max_length=1024)
    encoded_location = serializers.CharField(max_length=1024)
    status = StatusTypeField()
    type = AudioMediaTypeField()

class ImageMediaOutput(serializers.Serializer):
    name = serializers.CharField(max_length=255, allow_blank=False)
    location = serializers.CharField(max_length=1024)
    type = ImageMediaTypeField()

class VideoResponseSerializer(serializers.Serializer):
    id  = serializers.UUIDField()
    title = serializers.CharField(max_length=255, allow_blank=False)
    description = serializers.CharField(max_length=1024, allow_blank=False)
    duration = serializers.DecimalField(max_digits=10, decimal_places=2)
    rating = RatingTypeField()
    banner = ImageMediaOutput(allow_null=True)
    thumbnail = ImageMediaOutput(allow_null=True)
    thumbnail_half = ImageMediaOutput(allow_null=True)
    trailer = AudioVideoMediaOutput(allow_null=True)
    video = AudioVideoMediaOutput(allow_null=True)
    categories = SetField(child=serializers.UUIDField())
    genres = SetField(child=serializers.UUIDField())
    cast_members = SetField(child=serializers.UUIDField())
    created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    launch_at = serializers.DateField()
    published = serializers.BooleanField(default=False)

class ListVideoResponseSerializer(serializers.Serializer):
    data = VideoResponseSerializer(many=True)
    meta = ListOutputMetaSerializer()

class CreateVideoWithoutMediaRequestSerializer(serializers.Serializer):
    title           = serializers.CharField(max_length=255, allow_blank=False)
    description     = serializers.CharField(max_length=1024)
    duration        = serializers.DecimalField(max_digits=10, decimal_places=2)
    rating          = RatingTypeField()
    launch_at       = serializers.DateField()
    categories      = SetField(child=serializers.UUIDField())
    genres          = SetField(child=serializers.UUIDField())
    cast_members    = SetField(child=serializers.UUIDField())

class CreateVideoResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class UploadAudioMediaSerializer(serializers.Serializer):
    video_id        = serializers.UUIDField()
    video_file      = serializers.FileField()
    video_type      = AudioMediaTypeField()
    
# class DeleteGenreRequestSerializer(serializers.Serializer):
#     id = serializers.UUIDField()

# class UpdateGenreSerializer(serializers.Serializer):
#     id = serializers.UUIDField()
#     name = serializers.CharField(max_length=255, allow_blank=False)
#     is_active   = serializers.BooleanField()
#     categories_id = SetField(child=serializers.UUIDField())

# class PutGenreSerializer(serializers.Serializer):
#     id = serializers.UUIDField()
#     name = serializers.CharField(max_length=255, allow_blank=False, required=False)
#     is_active   = serializers.BooleanField(required=False)
#     categories_id = SetField(child=serializers.UUIDField(), required=False)
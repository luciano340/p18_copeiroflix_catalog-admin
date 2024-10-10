from email.policy import default
from rest_framework import serializers

from src.core.video.domain.value_objetcs import Rating
from src.django_project.apps._shared.serializers import ListOutputMetaSerializer

# class GenreResponseSerializer(serializers.Serializer):
#     id = serializers.UUIDField()
#     name = serializers.CharField(max_length=255, allow_blank=False)
#     is_active = serializers.BooleanField(default=True)
#     categories_id = serializers.ListField(child=serializers.UUIDField())
#     created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
#     updated_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

# class ListGenreResponseSerializer(serializers.Serializer):
#     data = GenreResponseSerializer(many=True)
#     meta = ListOutputMetaSerializer()
    
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

class UploadMediaSerializer(serializers.Serializer):
    video_id        = serializers.UUIDField()
    video_file      = serializers.FileField()

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
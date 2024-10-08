from email.policy import default
from rest_framework import serializers

from src.django_project.apps._shared.serializers import ListOutputMetaSerializer

class GenreResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, allow_blank=False)
    is_active = serializers.BooleanField(default=True)
    categories_id = serializers.ListField(child=serializers.UUIDField())
    created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

class ListGenreResponseSerializer(serializers.Serializer):
    data = GenreResponseSerializer(many=True)
    meta = ListOutputMetaSerializer()
    
class SetField(serializers.ListField):
    def to_internal_value(self, data):
        return set(super().to_internal_value(data))
    
    def to_representation(self, data):
        return list(super().to_representation(data))
    
class CreateGenreRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, allow_blank=False)
    is_active   = serializers.BooleanField(default=True)
    categories_id = SetField(child=serializers.UUIDField())

class CreateGenreResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class DeleteGenreRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class UpdateGenreSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, allow_blank=False)
    is_active   = serializers.BooleanField()
    categories_id = SetField(child=serializers.UUIDField())

class PutGenreSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, allow_blank=False, required=False)
    is_active   = serializers.BooleanField(required=False)
    categories_id = SetField(child=serializers.UUIDField(), required=False)
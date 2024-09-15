from email.policy import default
from rest_framework import serializers

from src.django_project.apps._shared.serializers import ListOutputMetaSerializer

class CategoryResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, allow_blank=False)
    description = serializers.CharField(max_length=1024)
    is_active   = serializers.BooleanField(default=True)
    created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

class ListCategoryResponseSerializer(serializers.Serializer):
    data = CategoryResponseSerializer(many=True)
    meta = ListOutputMetaSerializer()

class RetrieveCategoryResponseSerializer(serializers.Serializer):
    data = CategoryResponseSerializer(source="*")

class RetrieveCategoryRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class CreateCategoryRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, allow_blank=False)
    description = serializers.CharField(max_length=1024)
    is_active   = serializers.BooleanField(default=True)

class CreateCategoryResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class UpdateCategorySerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, allow_blank=False)
    description = serializers.CharField(max_length=1024)
    is_active   = serializers.BooleanField()

class PutCategorySerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(max_length=1024, required=False)
    is_active   = serializers.BooleanField(required=False)

class DeleteCategoryRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
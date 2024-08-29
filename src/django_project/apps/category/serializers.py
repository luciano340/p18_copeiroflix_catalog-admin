from email.policy import default
from rest_framework import serializers

class CategoryResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=1024)
    is_active   = serializers.BooleanField(default=True)
    created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

class ListCategoryResponseSerializer(serializers.Serializer):
    data = CategoryResponseSerializer(many=True)

class RetrieveCategoryResponseSerializer(serializers.Serializer):
    data = CategoryResponseSerializer(source="*")

class RetrieveCategoryRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class CreateCategoryRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=1024)
    is_active   = serializers.BooleanField(default=True)

class CreateCategoryResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
from email.policy import default
from rest_framework import serializers

class GenreResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, allow_blank=False)
    is_active = serializers.BooleanField(default=True)
    categories_id = serializers.ListField(child=serializers.UUIDField())
    created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

class ListGenreResponseSerializer(serializers.Serializer):
    data = GenreResponseSerializer(many=True)

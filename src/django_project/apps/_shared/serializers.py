from rest_framework import serializers

class ListOutputMetaSerializer(serializers.Serializer):
    current_page = serializers.IntegerField()
    page_size = serializers.IntegerField()
    total = serializers.IntegerField()
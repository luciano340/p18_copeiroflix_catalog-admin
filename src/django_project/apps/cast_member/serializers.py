from email.policy import default
from rest_framework import serializers

from src.core.cast_member.domain.cast_member import CastMemberType

class CastMemberTypeField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        choices = [(type.name, type.value) for type in CastMemberType]
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        return CastMemberType(super().to_internal_value(data))

    def to_representation(self, value):
        return str(super().to_representation(value))
    
class CastMemberResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, allow_blank=False)
    type = CastMemberTypeField()
    created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

class ListCastMemberResponseSerializer(serializers.Serializer):
    data = CastMemberResponseSerializer(many=True)

class RetrieveCastMemberResponseSerializer(serializers.Serializer):
    data = CastMemberResponseSerializer(source="*")

class RetrieveCastMemberRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class CreateCastMemberRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, allow_blank=False)
    type = CastMemberTypeField()

class CreateCastMemberResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class UpdateCastMemberSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, allow_blank=False)
    type = CastMemberTypeField()

class PutCastMemberSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, required=False)
    type = CastMemberTypeField( required=False)

class DeleteCastMemberRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()

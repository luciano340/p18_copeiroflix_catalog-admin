from uuid import UUID
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST

from src.core.cast_member.application.use_cases.create_cast_member import CreateCastMember, CreateCastMemberRequest
from src.core.cast_member.application.use_cases.delete_cast_member import DeleteCastMember, DeleteCastMemberRequest
from src.core.cast_member.application.use_cases.exceptions import CastMemberNotFound, CastMemberOrderNotFound
from src.core.cast_member.application.use_cases.get_caster_member import GetCastMember, GetCastMemberRequest
from src.core.cast_member.application.use_cases.list_cast_member import ListCastMember, RequestListCastMember
from src.core.cast_member.application.use_cases.update_cast_member import UpdateCastMember, UpdateCastMemberRequest
from src.django_project.apps.cast_member.repository import DjangoORMCastMemberRepository
from src.django_project.apps.cast_member.serializers import CreateCastMemberRequestSerializer, CreateCastMemberResponseSerializer, DeleteCastMemberRequestSerializer, ListCastMemberResponseSerializer, PutCastMemberSerializer, RetrieveCastMemberRequestSerializer, RetrieveCastMemberResponseSerializer, UpdateCastMemberSerializer


class CastMemberViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        order_by = request.query_params.get("order_by", "name")
        input = RequestListCastMember(
            order_by=order_by
        )
        use_case = ListCastMember(repository=DjangoORMCastMemberRepository())

        try:
            output = use_case.execute(input)
        except CastMemberOrderNotFound as err:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={
                    "error": str(err)
                }
            )
        
        serializer = ListCastMemberResponseSerializer(instance=output)

        return Response(
            status=HTTP_200_OK,
            data=serializer.data
        )

    def retrieve(self, request: Request, pk=None) -> Response:
        serializer = RetrieveCastMemberRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)
        
        use_case = GetCastMember(repository=DjangoORMCastMemberRepository())
        request_dto = GetCastMemberRequest(**serializer.validated_data)

        try:
            response_dto = use_case.execute(request=request_dto)
        except CastMemberNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        CastMember_output = RetrieveCastMemberResponseSerializer(instance=response_dto)
        return Response(
            status=HTTP_200_OK,
            data=CastMember_output.data
        )

    def create(self, request: Request) -> Response:
        serializer = CreateCastMemberRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        request_dto = CreateCastMemberRequest(**serializer.validated_data)
        use_case = CreateCastMember(repository=DjangoORMCastMemberRepository())
        output = use_case.execute(request=request_dto)

        return Response(
            status=HTTP_201_CREATED,
            data=CreateCastMemberResponseSerializer(instance=output).data
        )

    def update(self, request: Request, pk: UUID=None) -> Response:
        serializer = UpdateCastMemberSerializer(
            data={**request.data, "id":pk},
        )

        serializer.is_valid(raise_exception=True)
        request_dto = UpdateCastMemberRequest(**serializer.validated_data)
        use_case = UpdateCastMember(repository=DjangoORMCastMemberRepository())

        try:
            output = use_case.execute(request=request_dto)
        except CastMemberNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        
        return Response(status=HTTP_204_NO_CONTENT)

    def partial_update(self, request: Request, pk: UUID=None) -> Response:
        serializer = PutCastMemberSerializer(
            data={**request.data, "id":pk},
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        request_dto = UpdateCastMemberRequest(**serializer.validated_data)
        use_case = UpdateCastMember(repository=DjangoORMCastMemberRepository())

        try:
            output = use_case.execute(request=request_dto)
        except CastMemberNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        
        return Response(status=HTTP_204_NO_CONTENT)
    
    def destroy(self, request: Request, pk: UUID=None) -> Response:
        serializer = DeleteCastMemberRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        use_case = DeleteCastMember(repository=DjangoORMCastMemberRepository())
        request_dto = DeleteCastMemberRequest(id=serializer.validated_data['id'])

        try:
            output = use_case.execute(request=request_dto)
        except CastMemberNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        
        return Response(status=HTTP_204_NO_CONTENT)
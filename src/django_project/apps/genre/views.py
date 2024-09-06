from uuid import UUID
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT

from src.core.genre.application.use_cases.create_genre import CreateGenre, CreateGenreRequest
from src.core.genre.application.use_cases.delete_genre import DeleteGenre, DeleteGenreRequest
from src.core.genre.application.use_cases.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.application.use_cases.list_genre import ListGenre, RequestListGenre
from src.django_project.apps.category.repository import DjangoORMCategoryRepository
from src.django_project.apps.genre.repository import DjangoORMGenreRepository
from src.django_project.apps.genre.serializers import CreateGenreRequestSerializer, CreateGenreResponseSerializer, DeleteGenreRequestSerializer, ListGenreResponseSerializer

class GenreViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        use_case = ListGenre(repository=DjangoORMGenreRepository())
        output = use_case.execute(request=RequestListGenre())
        
        response = ListGenreResponseSerializer(output)

        return Response(
            status=HTTP_200_OK,
            data=response.data
        )

    def create(self, request: Request) -> Response:
        serializer = CreateGenreRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        request_dto = CreateGenreRequest(**serializer.validated_data)
        use_case = CreateGenre(
            repository=DjangoORMGenreRepository(), 
            category_repository=DjangoORMCategoryRepository()
        )

        try:
            output = use_case.execute(request=request_dto)
        except (InvalidGenre, RelatedCategoriesNotFound) as err:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={
                    "error": str(err)
                }
            )

        return Response(
            status=HTTP_201_CREATED,
            data=CreateGenreResponseSerializer(instance=output).data
        )

    def destroy(self, request: Request, pk: UUID=None) -> Response:
        serializer = DeleteGenreRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        use_case = DeleteGenre(repository=DjangoORMGenreRepository())
        request_dto = DeleteGenreRequest(id=serializer.validated_data['id'])

        try:
            output = use_case.execute(request=request_dto)
        except GenreNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        
        return Response(status=HTTP_204_NO_CONTENT)
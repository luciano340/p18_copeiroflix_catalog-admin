from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from src.core.genre.application.use_cases.list_genre import ListGenre, RequestListGenre
from src.django_project.apps.genre.repository import DjangoORMGenreRepository
from src.django_project.apps.genre.serializers import ListGenreResponseSerializer

class GenreViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        use_case = ListGenre(repository=DjangoORMGenreRepository())
        output = use_case.execute(request=RequestListGenre())
        
        response = ListGenreResponseSerializer(output)

        return Response(
            status=HTTP_200_OK,
            data=response.data
        )
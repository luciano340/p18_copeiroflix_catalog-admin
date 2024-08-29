from urllib import response
from uuid import UUID
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest
from src.core.category.application.use_cases.list_category import ListCategory, ListCategoryRequest
from django_project.apps.category.repository import DjangoORMCategoryRepository
from src.django_project.apps.category.serializers import CategoryResponseSerializer, ListCategoryResponseSerializer, RetrieveCategoryRequestSerializer


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        input = ListCategoryRequest
        use_case = ListCategory(repository=DjangoORMCategoryRepository())
        output = use_case.execute(input)
        
        serializer = ListCategoryResponseSerializer(instance=output)

        return Response(
            status=HTTP_200_OK,
            data=serializer.data
        )

    def retrieve(self, request: Request, pk=None):
        serializer = RetrieveCategoryRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)
        
        use_case = GetCategory(repository=DjangoORMCategoryRepository())
        request_dto = GetCategoryRequest(id=serializer.validated_data["id"])

        try:
            response_dto = use_case.execute(request=request_dto)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        category_output = CategoryResponseSerializer(instance=response_dto)
        return Response(
            status=HTTP_200_OK,
            data=category_output.data
        )
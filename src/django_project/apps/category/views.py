from ast import Return
import re
from urllib import response
from uuid import UUID
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from src.core.category.application.use_cases.create_category import CreateCategory, CreateCategoryRequest
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest
from src.core.category.application.use_cases.list_category import ListCategory, ListCategoryRequest
from django_project.apps.category.repository import DjangoORMCategoryRepository
from src.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from src.django_project.apps.category import repository
from src.django_project.apps.category.serializers import CategoryResponseSerializer, CreateCategoryRequestSerializer, CreateCategoryResponseSerializer, ListCategoryResponseSerializer, RetrieveCategoryRequestSerializer, RetrieveCategoryResponseSerializer, UpdateCategorySerializer


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

    def retrieve(self, request: Request, pk=None) -> Response:
        serializer = RetrieveCategoryRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)
        
        use_case = GetCategory(repository=DjangoORMCategoryRepository())
        request_dto = GetCategoryRequest(**serializer.validated_data)

        try:
            response_dto = use_case.execute(request=request_dto)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        category_output = RetrieveCategoryResponseSerializer(instance=response_dto)
        return Response(
            status=HTTP_200_OK,
            data=category_output.data
        )

    def create(self, request: Request) -> Response:
        serializer = CreateCategoryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        request_dto = CreateCategoryRequest(**serializer.validated_data)
        use_case = CreateCategory(repository=DjangoORMCategoryRepository())
        output = use_case.execute(request=request_dto)

        return Response(
            status=HTTP_201_CREATED,
            data=CreateCategoryResponseSerializer(instance=output).data
        )

    def update(self, request: Request, pk=None) -> Response:
        serializer = UpdateCategorySerializer(
            data={**request.data, "id":pk},
        )

        serializer.is_valid(raise_exception=True)
        request_dto = UpdateCategoryRequest(**serializer.validated_data)
        use_case = UpdateCategory(repository=DjangoORMCategoryRepository())

        try:
            output = use_case.execute(request=request_dto)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        
        return Response(status=HTTP_204_NO_CONTENT)
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


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        input = ListCategoryRequest
        use_case = ListCategory(repository=DjangoORMCategoryRepository())
        output = use_case.execute(input)
        
        categories = [
            {
                "id": str(category.id),
                "name": category.name,
                "description": category.description,
                "is_active": category.is_active,
                "created_date": category.created_date.strftime('%Y-%m-%d %H:%M:%S'),
                "updated_date": category.updated_date if not category.updated_date else category.updated_date.strftime('%Y-%m-%d %H:%M:%S')
            }
            for category in output.data
        ]

        return Response(
            status=HTTP_200_OK,
            data=categories
        )

    def retrieve(self, request: Request, pk=None):
        try:
            category_pk = UUID(pk)
        except ValueError:
            return Response(status=HTTP_400_BAD_REQUEST)
        
        use_case = GetCategory(repository=DjangoORMCategoryRepository())
        request_dto = GetCategoryRequest(id=category_pk)

        try:
            response_dto = use_case.execute(request=request_dto)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        category_output = {
            "id": str(response_dto.id),
            "name": response_dto.name,
            "description": response_dto.description,
            "is_active": response_dto.is_active,
            "created_date": response_dto.created_date,
            "updated_date": response_dto.updated_date
        }

        return Response(
            status=HTTP_200_OK,
            data=category_output
        )
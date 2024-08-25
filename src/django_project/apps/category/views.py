from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK
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
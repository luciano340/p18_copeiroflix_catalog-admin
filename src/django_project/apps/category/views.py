from uuid import UUID
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from src.core.category.application.use_cases.create_category import CreateCategory, CreateCategoryRequest
from src.core.category.application.use_cases.delete_category import DeleteCategory, DeleteCategoryRequest
from src.core.category.application.use_cases.exceptions import CategoryNotFound, CategoryOrderNotFound
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest
from src.core.category.application.use_cases.list_category import ListCategory, ListCategoryRequest
from src.django_project.apps.category.repository import DjangoORMCategoryRepository
from src.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from src.django_project.apps.category.serializers import CreateCategoryRequestSerializer, CreateCategoryResponseSerializer, DeleteCategoryRequestSerializer, ListCategoryResponseSerializer, PutCategorySerializer, RetrieveCategoryRequestSerializer, RetrieveCategoryResponseSerializer, UpdateCategorySerializer


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        order_by = request.query_params.get("order_by", "name")
        try:
            current_page = int(request.query_params.get("current_page", 1))
        except ValueError as err:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={
                    "error": "Invalid page number"
                }
            )
        
        input = ListCategoryRequest(
            order_by=order_by,
            current_page=current_page
        )
        use_case = ListCategory(repository=DjangoORMCategoryRepository())

        try:
            output = use_case.execute(input)
        except CategoryOrderNotFound as err:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={
                    "error": str(err)
                }
            )
        
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

    def update(self, request: Request, pk: UUID=None) -> Response:
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

    def partial_update(self, request: Request, pk: UUID=None) -> Response:
        serializer = PutCategorySerializer(
            data={**request.data, "id":pk},
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        request_dto = UpdateCategoryRequest(**serializer.validated_data)
        use_case = UpdateCategory(repository=DjangoORMCategoryRepository())

        try:
            output = use_case.execute(request=request_dto)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        
        return Response(status=HTTP_204_NO_CONTENT)
    
    def destroy(self, request: Request, pk: UUID=None) -> Response:
        serializer = DeleteCategoryRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        use_case = DeleteCategory(repository=DjangoORMCategoryRepository())
        request_dto = DeleteCategoryRequest(id=serializer.validated_data['id'])

        try:
            output = use_case.execute(request=request_dto)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        
        return Response(status=HTTP_204_NO_CONTENT)
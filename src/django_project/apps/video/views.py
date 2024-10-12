from uuid import UUID
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT, HTTP_500_INTERNAL_SERVER_ERROR

from src.core._shared.infra.storage.local_storage import LocalStorage
from src.core.video.application.use_cases.create_video_without_media import CreateVideoWithoutMedia, RequestCreateVideoWithoutMedia
from src.core.video.application.use_cases.exceptions import AudioVideoMediaError, InvalidVideo, RelatedEntitiesNotFound, VideoNotFound
from src.core.video.application.use_cases.list_video import ListVideo, RequestListVideo
from src.core.video.application.use_cases.upload_video import RequestUploadVideo, UploadVideo
from src.django_project.apps.cast_member.repository import DjangoORMCastMemberRepository
from src.django_project.apps.category.repository import DjangoORMCategoryRepository
from src.django_project.apps.genre.repository import DjangoORMGenreRepository
from src.django_project.apps.video.repository import DjangoORMVideoRepository
from src.django_project.apps.video.serializers import CreateVideoResponseSerializer, CreateVideoWithoutMediaRequestSerializer, ListVideoResponseSerializer, UploadAudioMediaSerializer

class VideoViewSet(viewsets.ViewSet):
    def create(self, request: Request) -> Response:
        serializer = CreateVideoWithoutMediaRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        request_dto = RequestCreateVideoWithoutMedia(**serializer.validated_data)
        use_case = CreateVideoWithoutMedia(
            video_repository=DjangoORMVideoRepository(),
            genre_repository=DjangoORMGenreRepository(),
            category_repository=DjangoORMCategoryRepository(),
            cast_member_repository=DjangoORMCastMemberRepository()
        )

        try:
            output = use_case.execute(request=request_dto)
        except (InvalidVideo, RelatedEntitiesNotFound) as err:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={
                    "error": str(err)
                }
            )

        return Response(
            status=HTTP_201_CREATED,
            data=CreateVideoResponseSerializer(instance=output).data
        )

    def list(self, request: Request) -> Response:
        order_by = request.query_params.get("order_by", "title")
        try:
            current_page = int(request.query_params.get("current_page", 1))
        except ValueError as err:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={
                    "error": "Invalid page number"
                }
            )
        use_case = ListVideo(repository=DjangoORMVideoRepository())
        output = use_case.execute(request=RequestListVideo(order_by=order_by, current_page=current_page))
        
        response = ListVideoResponseSerializer(output)

        return Response(
            status=HTTP_200_OK,
            data=response.data
        )

class VideoMediaViewSet(viewsets.ViewSet):
    def partial_update(self, request: Request, pk: UUID) -> Response:
        serializer = UploadAudioMediaSerializer(
            data={
                "video_id": pk,
                "video_file": request.FILES["video_file"],
                "video_type": request.data.get("video_type")
            },
        )
        serializer.is_valid(raise_exception=True)

        upload_video = UploadVideo(
            video_repository=DjangoORMVideoRepository(),
            storage_service=LocalStorage()
        )

        request_upload_video = RequestUploadVideo(
            video_id=serializer.validated_data["video_id"],
            file_name=serializer.validated_data["video_file"],
            content=serializer.validated_data["video_file"].read(),
            content_type=serializer.validated_data["video_file"].content_type,
            video_type=serializer.validated_data['video_type']
        )

        try:
            upload_video.execute(request=request_upload_video)
        except VideoNotFound as err:
            return Response(status=HTTP_404_NOT_FOUND, data={"error": str(err)})
        except AudioVideoMediaError as err:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                data={
                    "error": str(err)
                }
            )
        return Response(status=200)
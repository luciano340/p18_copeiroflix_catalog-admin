from uuid import UUID
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT

from src.core._shared.infra.storage.local_storage import LocalStorage
from src.core.video.application.use_cases.create_video_without_media import CreateVideoWithoutMedia, RequestCreateVideoWithoutMedia
from src.core.video.application.use_cases.exceptions import InvalidVideo, RelatedEntitiesNotFound, VideoNotFound
from src.core.video.application.use_cases.upload_video import RequestUploadVideo, UploadVideo
from src.django_project.apps.cast_member.repository import DjangoORMCastMemberRepository
from src.django_project.apps.category.repository import DjangoORMCategoryRepository
from src.django_project.apps.genre.repository import DjangoORMGenreRepository
from src.django_project.apps.video.repository import DjangoORMVideoRepository
from src.django_project.apps.video.serializers import CreateVideoResponseSerializer, CreateVideoWithoutMediaRequestSerializer

class VideoMnediaViewSet(viewsets.ViewSet):
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

    def partial_update(self, request: Request, pk: UUID) -> Response:
        file = request.FILES["video_file"]
        content = file.read()
        content_type = file.content_type

        upload_video = UploadVideo(
            video_repository=DjangoORMVideoRepository(),
            storage_service=LocalStorage()
        )

        request_upload_video = RequestUploadVideo(
            video_id=UUID(pk),
            file_name=file.name,
            content=content,
            content_type=content_type
        )

        try:
            upload_video.execute(request=request_upload_video)
        except VideoNotFound as err:
            return Response(status=HTTP_404_NOT_FOUND, data={"error": str(err)})
    
        return Response(status=200)
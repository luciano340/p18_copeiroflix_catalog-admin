"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from src.django_project.apps.cast_member.views import CastMemberViewSet
from src.django_project.apps.category.views import CategoryViewSet
from src.django_project.apps.genre.views import GenreViewSet
from src.django_project.apps.video.views import VideoMnediaViewSet


router = DefaultRouter()
router.register(r'api/categories', CategoryViewSet, basename="category")
router.register(r'api/genres', GenreViewSet, basename="genre")
router.register(r'api/cast_members', CastMemberViewSet, basename="cast_member")
router.register(r'api/videos', VideoMnediaViewSet, basename="video_without_media")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django_prometheus.urls')),
] + router.urls

# urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import BookmarkViewSet

router = DefaultRouter()
router.register(r'bookmarks', BookmarkViewSet, basename='bookmark')

urlpatterns = [
    path('', include(router.urls)),
]

from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import BookViewset, GenreViewset


router = DefaultRouter()
router.register('genres', GenreViewset)
router.register('books', BookViewset)

urlpatterns = [
    path('', include(router.urls))
]
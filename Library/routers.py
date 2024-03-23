
from rest_framework.routers import DefaultRouter

from app1.viewsets import BookViewSet

router = DefaultRouter()
router.register('books',BookViewSet, basename='books')

urlpatterns=router.urls
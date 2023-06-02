from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

router = DefaultRouter()

router.register('category', CategoryViewSet, basename='category')
router.register(
    r'reviews/(?P<title_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('/', include(router.urls)),
]

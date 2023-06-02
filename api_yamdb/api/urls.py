from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

app_name = 'api'
router_v1 = DefaultRouter()

router_v1.register('/categories/', CategoryViewSet, basename='category')
router_v1.register('/genres/', GenreViewSet, basename='genres')
router_v1.register('/titles/', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d{1,})/',
    TitleViewSet,
    basename='titles',
)

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router_v1.urls)),
]

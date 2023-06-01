from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CommentViewSet, ReviewViewSet


app_name = 'api'
router_v1 = DefaultRouter()

router_v1.register(
    r'titles/(?P<title_id>\d{1,})/reviews/(?P<review_id>\d{1,})/comments',
    CommentViewSet,
    basename='comments'
)
router_v1.register(
    r'titles/(?P<title_id>\d{1,})/reviews',
    ReviewViewSet,
    basename='reviews'
)

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router_v1.urls)),
]

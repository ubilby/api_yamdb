from rest_framework import viewsets
# from rest_framework.filters import SearchFilter
# from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny

from reviews.models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
# from .permissions import


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        return serializer.save()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        return serializer.save()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        return serializer.save()

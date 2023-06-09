from re import match

from django.contrib.auth.tokens import default_token_generator
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, MyUser, Rating, Review, Title

from .filters import TitlesFilter
from .mixins import MultiMixin
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrModeratorOrAdmin
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, SignupSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          TokenSerializer, UserSerializer)
from .utils import token_to_email


class UserViewSet(ModelViewSet):
    lookup_field = 'username'
    search_fields = ('username',)
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=["get", "patch"],
        detail=False,
        url_path="me",
        permission_classes=(IsAuthenticated,),
    )
    def users_own_profile(self, request):
        user = request.user
        if request.method == "PATCH":
            serializer = self.get_serializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)

            if 'username' in serializer.validated_data:
                username = serializer.validated_data['username']
                if not match(r'^[\w.@+-]+$', username):
                    return Response(
                        {'detail': 'Неверный формат поля username.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            serializer.save()
        else:
            serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def sign_up(request):
    # для регистрации
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, _ = MyUser.objects.get_or_create(**serializer.validated_data)
    except IntegrityError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    confirmation_code = default_token_generator.make_token(user)
    email = user.email
    token_to_email(email, confirmation_code)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def get_token(request):
    # для получения токена
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']
    user = get_object_or_404(MyUser, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response({f'{token}'}, status=status.HTTP_200_OK)
    return Response({'confirmation_code': 'Неверный код подтверждения'},
                    status=status.HTTP_400_BAD_REQUEST)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    # lookup_field = 'slug'
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)

    # фильтры, возможно придётся удалить?
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer

    def perform_create(self, serializer):
        # Сохранение тайтла и получение созданного объекта
        title = serializer.save()

        Rating.objects.create(title=title)
        return Response(
            {'title': TitleReadSerializer(title).data},
            status=status.HTTP_201_CREATED
        )


class CategoryViewSet(MultiMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ('name',)
    lookup_field = 'slug'
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter, )


class GenreViewSet(MultiMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter, )
    search_fields = ('name',)
    lookup_field = 'slug'
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrModeratorOrAdmin, )

    def perform_create(self, serializer):
        author = self.request.user
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        titles = Title.objects.filter(reviews__author=author)
        if title in titles:
            raise exceptions.ValidationError('У вас уже есть отзыв')
        serializer.save(
            author=author,
            title=title
        )

    def get_queryset(self):
        review = Review.objects.filter(title_id=self.kwargs.get('title_id'))
        return review.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrModeratorOrAdmin, )

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        )

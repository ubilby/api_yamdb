import re

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from reviews.models import Category, Comment, Genre, MyUser, Review, Title
from .validators import username_validator


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug',)
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug',)
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(
        read_only=True,
    )
    genre = GenreSerializer(
        read_only=True,
        many=True,
    )
    rating = serializers.SlugRelatedField(
        slug_field='average_score',
        read_only=True,
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')

        search_fields = ('category', 'genre', 'name')


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = (
            "id",
            "text",
            "author",
            "score",
            "pub_date"
        )
        model = Review
        read_only_fields = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)


class UserSerializer(ModelSerializer):
    username = serializers.RegexField(
        regex=r'[\w.@+-]+\Z',
        max_length=150,
        required=True
    )

    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        read_only_fields = ("role",)
        model = MyUser

    def validate_username(self, value):
        pattern = r'^[\w.@+-]+\Z'
        if re.match(pattern, value) is None:
            raise serializers.ValidationError('error!')
        return value


# class UserCreateSerializer(UserSerializer):
#     class Meta:
#         read_only_fields = ("role",)
#         username = serializers.RegexField(
#             regex=r'[\w.@+-]+$',
#             max_length=64,
#             required=True,
#         )

#         email = serializers.EmailField(
#             max_length=256,
#             required=True,
#         )
#         model = MyUser
#         fields = ('username',
#                   'email',
#                   'first_name',
#                   'last_name',
#                   'bio',
#                   'role')

#     def validate_username(self, value):
#         return username_validator(value)


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
    )

    class Meta:
        fields = ('email', 'username')
        model = MyUser

    def validate_username(self, value):
        pattern = r'^[\w.@+-]+\Z'
        if re.match(pattern, value) is None:
            raise serializers.ValidationError('error!')
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

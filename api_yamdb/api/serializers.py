import re

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from reviews.models import Category, Comment, Genre, MyUser, Review, Title
from django.core.exceptions import ValidationError
from django.utils import timezone


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
    )
    genre = GenreSerializer(
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
        read_only_fields = ('category', 'genre')
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

    def validate_year(self, creation_year):
        if creation_year > timezone.now().year:
            raise ValidationError(
                f'Год не может быть больше {timezone.now().year}'
            )
        return creation_year

    def validate_genre(self, genre):
        if genre == []:
            raise ValidationError('Жанр не может быть пустым')
        return genre


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
        required=True,
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
        model = MyUser

    def validate_role(self, value):
        roles = [choice[0] for choice in MyUser.ROLE_CHOICES]
        if value not in roles:
            raise serializers.ValidationError('Несуществующая роль.')
        return value

    def validate_username(self, value):
        pattern = r'^[\w.@+-]+\Z'
        if re.match(pattern, value) is None:
            raise serializers.ValidationError('error!')
        if MyUser.objects.filter(username=value).exists():
            raise serializers.ValidationError('error!')
        return value


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

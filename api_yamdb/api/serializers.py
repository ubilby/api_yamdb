from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = ('name', 'year', 'genre', 'category', 'description')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')

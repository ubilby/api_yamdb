import re

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_year


class MyUser(AbstractUser):
    ROLE_USER = 'user'
    ROLE_MODERATOR = 'moderator'
    ROLE_ADMIN = 'admin'

    ROLE_CHOICES = (
        (ROLE_USER, 'user'),
        (ROLE_MODERATOR, 'moderator'),
        (ROLE_ADMIN, 'admin'),
    )

    def username_validator(value):
        pattern = r'^[\w.@+-]+\Z'
        if re.match(pattern, value) is None:
            raise ValidationError('error')

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator]
    )
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=64,
        choices=ROLE_CHOICES,
        default=ROLE_USER
    )
    bio = models.TextField(blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    confirmation_code = models.CharField(
        max_length=64,
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Юзверь'
        verbose_name_plural = 'Юзвери'
        ordering = ("username",)
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username="me"), name="name_not_me"
            )
        ]

    @property
    def is_moderator(self):
        return self.role == self.ROLE_MODERATOR

    @property
    def is_admin(self):
        return self.role == (self.ROLE_ADMIN
                             or self.is_superuser
                             or self.is_staff)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField(validators=(validate_year,))
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
        blank=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class ReviewManager(models.Manager):
    def create(self, **kwargs):
        title = kwargs.get('title')
        author = kwargs.get('author')
        if title and author:
            if self.filter(title=title, author=author).exists():
                return None
        return super().create(**kwargs)


class Review(models.Model):
    objects = ReviewManager()
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Отзыв',
    )
    author = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    text = models.TextField(
        'Текст отзыва',
        help_text='Введите отзыв',
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.title.rating:
            self.title.rating.update_average_score()
        else:
            self.title.rating = Rating.objects.create(
                title=self.title,
                average_score=self.score
            )

    def delete(self, *args, **kwargs):
        self.title.rating.update_average_score()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='unique_title_author')
        ]

    def __str__(self):
        return self.text


class Rating(models.Model):
    title = models.OneToOneField(
        Title,
        on_delete=models.CASCADE,
        related_name='rating',
        null=True,
        blank=True
    )
    average_score = models.IntegerField(
        null=True
    )

    def __str__(self):
        return str(self.average_score)

    def __repr__(self):
        return str(self.average_score)

    def update_average_score(self):
        reviews = self.title.reviews.all()
        if reviews:
            total_score = sum(review.score for review in reviews)
            self.average_score = round(total_score / len(reviews))
        else:
            self.average_score = 0
        self.save()


class Comment(models.Model):
    author = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text

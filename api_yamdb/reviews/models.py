from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_year


class MyUser(AbstractUser):
    ROLE_USER = 0
    ROLE_MODERATOR = 1
    ROLE_ADMIN = 2

    ROLE_CHOICES = (
        (ROLE_USER, 'User'),
        (ROLE_MODERATOR, 'Moderator'),
        (ROLE_ADMIN, 'Admin'),
    )

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    role = models.IntegerField(choices=ROLE_CHOICES, default=ROLE_USER)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

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
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True,
        blank=True,
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Жанр',
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        created = not self.pk  # Проверяем, является ли экземпляр новым
        super().save(*args, **kwargs)  # Сохраняем экземпляр Title

        if created:  # Если экземпляр был только что создан
            Rating.objects.create(title=self, average_score=0)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return self.name


class Review(models.Model):
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

    def __str__(self):
        return self.text


class Rating(models.Model):
    title = models.OneToOneField(
        Title,
        on_delete=models.CASCADE,
        related_name='rating'
    )
    average_score = models.IntegerField(
        default=0,
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
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created',)

    def __str__(self):
        return self.text

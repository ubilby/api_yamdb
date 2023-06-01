from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class MyUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    is_user = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=256, required=True)
    slug = models.SlugField(max_length=50, required=True, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200, required=True)
    slug = models.SlugField(max_length=50, required=True, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256, required=True)
    year = models.IntegerField(required=True)
    description = models.CharField
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        required=True,
        related_name='titles',
        verbose_name='Категория',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        required=True,
        related_name='genres',
        verbose_name='Жанр',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return self.name


class Reviews(models.Model):
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
        required=True
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
    )
    score = models.IntegerField(
        required=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-created',)

    def __str__(self):
        return self.text


class Rating(models.Model):
    title = models.OneToOneField(
        Title, on_delete=models.CASCADE,
        related_name='rating'
    )
    average_score = models.DecimalField(max_digits=2, decimal_places=1)

    def update_average_score(self):
        # метод будет вызываться при удалении и добавлении Reviews
        # надо только понять когда это будет происходить
        reviews = self.title.reviews.all()
        if reviews:
            total_score = sum(review.score for review in reviews)
            self.average_score = total_score / len(reviews)
        else:
            self.average_score = 0
        self.save()


class Comment(models.Model):
    author = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Reviews, on_delete=models.CASCADE, related_name='comments'
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

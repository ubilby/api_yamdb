from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_year, username_validator


class MyUser(AbstractUser):
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    ROLE_USER = 'user'
    ROLE_MODERATOR = 'moderator'
    ROLE_ADMIN = 'admin'

    ROLE_CHOICES = (
        (ROLE_USER, 'user'),
        (ROLE_MODERATOR, 'moderator'),
        (ROLE_ADMIN, 'admin'),
    )

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


class AbstractModelCG(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Category(AbstractModelCG):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(AbstractModelCG):

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.PositiveSmallIntegerField(validators=(validate_year,))
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


class Rating(models.Model):
    title = models.OneToOneField(
        Title,
        on_delete=models.CASCADE,
        related_name='rating',
        null=True,
        blank=True
    )
    average_score = models.PositiveSmallIntegerField(
        null=True,
        default=None
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
        self.save()


class ReviewCommentBase(models.Model):
    author = models.ForeignKey(
        'MyUser',
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text


class Review(ReviewCommentBase):
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    def save(self, *args, **kwargs):
        if self.title.rating:
            self.title.rating.update_average_score()
        else:
            self.title.rating = Rating.objects.create(
                title=self.title,
                average_score=self.score
            )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]


class Comment(ReviewCommentBase):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'

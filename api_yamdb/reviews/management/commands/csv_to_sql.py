import csv
import os

from django.core.management.base import BaseCommand
from django.forms import ValidationError
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from reviews.models import MyUser, Category, Genre, Review, Comment, Title, Rating


class Command(BaseCommand):
    help = 'Imports data from CSV files to DB'

    files_models = {
        'users.csv': MyUser,
        'category.csv': Category,
        'genre.csv': Genre,
        'titles.csv': Title,
        'review.csv': Review,
        'comments.csv': Comment,
    }

    def handle(self, *args, **options):
        for file, model in self.files_models.items():
            path = os.path.realpath(
                f'/Users/ubilby/codes/python/ya_practicum/sprint_10/api_yamdb/api_yamdb/static/data/{file}'
            )
            with open(path, 'r', encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter=',')
                for row in reader:
                    try:
                        if 'category' in row:
                            category_id = int(row['category'])
                            try:
                                category = Category.objects.get(id=category_id)
                            except ObjectDoesNotExist:
                                raise ValueError(
                                    f"Category with id {category_id} does not exist.")
                            row['category'] = category

                        if 'genre' in row:
                            genre_ids = [
                                int(g) for g in row['genre'].split(',')
                            ]
                            genres = Genre.objects.filter(id__in=genre_ids)
                            if len(genres) != len(genre_ids):
                                raise ValueError(
                                    "One or more genres do not exist.")
                            row['genre'] = genres

                        if 'author' in row:
                            author_id = int(row['author'])
                            author = MyUser.objects.get(id=author_id)
                            row['author'] = author

                        record = model(**row)
                    except IntegrityError as e:
                        print(e)
                    else:
                        record.save()

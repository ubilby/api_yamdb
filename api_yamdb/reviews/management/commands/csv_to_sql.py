import csv
import os

from django.core.management.base import BaseCommand
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
            print(f'{file_} - {model}')  # тестовый принт имён файла и модели
            with open(path, 'r', encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter=',')
                for row in reader:
                    if 'category' in row:
                        category_id = int(row['category'])
                        category = Category.objects.get(id=category_id)
                        row['category'] = category

                    if 'genre' in row:
                        genre_ids = [
                            int(g) for g in row['genre'].split(',')
                        ]
                        genres = Genre.objects.filter(id__in=genre_ids)
                        row['genre'] = genres

                    if 'author' in row:
                        author_id = int(row['author'])
                        author = MyUser.objects.get(id=author_id)
                        row['author'] = author

                    record = model(**row)
                    record.save()

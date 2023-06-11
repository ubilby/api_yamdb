import csv
import os

from django.core.management.base import BaseCommand

from api_yamdb.settings import BASE_DIR
from reviews.models import Category, Comment, Genre, MyUser, Review, Title


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
        for file_, model in self.files_models.items():
            path = os.path.join(BASE_DIR, 'static', 'data', file_)
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

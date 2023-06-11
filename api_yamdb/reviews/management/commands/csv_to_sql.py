import csv
import os

from django.core.management.base import BaseCommand

from reviews.forms import (
    CategoryForm, GenreForm, TitleForm, CommentForm, ReviewForm, MyUserForm
)


class Command(BaseCommand):
    help = 'Imports data from CSV files to DB'
    files_models = {
        'users.csv': MyUserForm,
        'category.csv': CategoryForm,
        'genre.csv': GenreForm,
        'titles.csv': TitleForm,
        'review.csv': ReviewForm,
        'comments.csv': CommentForm,

    }

    def handle(self, *args, **options):
        # path = os.path.realpath(
        #     '.\\static\\data\\titles.csv'
        # )
        # with open(path, 'r', encoding="utf-8") as f:
        #     reader = csv.DictReader(f, delimiter=',')
        #     for row in reader:
        #         print(row)
        #         form = TitleForm(row)
        #         print(form.errors)
        #         form.save

        for file_, model in self.files_models.items():
            path = os.path.realpath(
                f'.\\static\\data\\{file_}'
            )
            print(f'{file_} - {model}')  # тестовый принт имён файла и модели
            with open(path, 'r', encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter=',')
                for row in reader:
                    print(row)
                    form = model(row)
                    print(form.errors)
                    new_id = form.save(commit=False)
                    new_id.id = row['id']
                    new_id.save()

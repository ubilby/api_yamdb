import csv
import os

from django.core.management.base import BaseCommand
from django.forms import ValidationError

from reviews.forms import (
    CategoryForm, GenreForm, TitleForm, CommentForm, ReviewForm, MyUserForm
)
# from reviews.models import MyUser, Category, Genre, Review, Comment, Title


class Command(BaseCommand):
    help = 'Imports data from CSV files to DB'

    files = (
        'users.csv',
        'category.csv',
        'genre.csv',
        'review.csv',
        'titles.csv',
        'comments.csv',
    )
    models = (
        MyUserForm,
        CategoryForm,
        GenreForm,
        ReviewForm,
        TitleForm,
        CommentForm,
    )
    files_models = {
        'users.csv': MyUserForm,
        'category.csv': CategoryForm,
        'genre.csv': GenreForm,
        'review.csv': ReviewForm,
        'titles.csv': TitleForm,
        'comments.csv': CommentForm,
    }

    def handle(self, *args, **options):
        for file_, model in self.files_models.items():
            path = os.path.realpath(
                f'.\\static\\data\\{file_}'
            )
            print(f'{file_} - {model}')  # тестовый принт имён файла и модели
            # a = 'a'  # музыкальная пауза
            # input(a)  # для разглядывания строчки словаря
            with open(path, 'r', encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter=',')
                # data = reader(file_)
                for row in reader:
                    print(row)
                    form = model(data=row)
                    print(form.errors)
                    # a = 'a'  # музыкальная пауза
                    # input(a)  # для разглядывания строчки словаря
                    if form.is_valid:
                        form.save()
                    else:
                        print(form.errors)
                        raise ValidationError('у вас Егор')

    # def csv_to_dict(self, file_name):
    #     path = os.path.realpath(f'.\\static\\data\\{file_name}')
    #     with open(path, 'r', encoding="utf-8") as f:
    #         reader = csv.DictReader(f, delimiter=',')
    #         return list(reader)

    # def handle(self, *args, **options):
    #     data = self.csv_to_dict('users.csv')
    #     for row in data:
    #         # form = MyUserForm(data=row)
    #         # form.save()
    #         MyUser.objects.create(data)

    #     data = self.csv_to_dict('category.csv')
    #     for row in data:
    #         form = CategoryForm(data=row)
    #         form.save()

    #     data = self.csv_to_dict('genre.csv')
    #     for row in data:
    #         form = GenreForm(data=row)
    #         form.save()

    #     data = self.csv_to_dict('review.csv')
    #     for row in data:
    #         form = ReviewForm(data=row)
    #         form.save()

    #     data = self.csv_to_dict('titles.csv')
    #     for row in data:
    #         form = TitleForm(data=row)
    #         form.save()

    #     data = self.csv_to_dict('comments.csv')
    #     for row in data:
    #         form = CommentForm(data=row)
    #         form.save()

        # data = self.csv_to_dict('genre_title.csv')
        # for row in data:
        #     if row[0] != 'id':

    # def main():
    #     con = sqlite3.connect('api_yamdb/db.sqlite3')
    #     cur = con.cursor
    #     data = csv_to_dict('users.csv')
    #     for dict_list in data:
    #         cur.execute(
    #             "INSERT INTO reviews_customuser VALUES "
    #             " (:id, '', '', '', :email, :username, :first_name, "
    #             " :last_name, '', :bio, '', :role)",
    #             dict_list
    #         )
    #     data = csv_to_dict('genre.csv')
    #     for dict_list in data:
    #         cur.execute(
    #             "INSERT INTO reviews_genre VALUES (:id, :name, :slug)",
    #             dict_list
    #         )

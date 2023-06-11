import csv
import os

from django.core.management.base import BaseCommand

from reviews.forms import (
    CategoryForm, GenreForm, TitleForm, CommentForm, ReviewForm, MyUserForm
)


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

    # def handle(self, *args, **options):
    #     for file, model in self.files_models:  # перебор файлов и моделей
    #         path = os.path.realpath(
    #             f'.\\api_yamdb\\static\\data\\{file}'  # берём файл с диска
    #         )
    #         print(f'{file} - {model}')  # тестовый принт имён файла и модели
    #         with open(path, 'r', encoding="utf-8") as f:
    #             reader = csv.DictReader(f, delimiter=',')
    #             data = reader(file)
    #             for row in data:
    #                 if row[0] != 'id':  # игнорируем первую строку
    #                     form = model(data=row)
    #                     if form.is_valid:
    #                         form.save()

    def csv_to_dict(self, file_name):
        path = os.path.realpath(f'.\\static\\data\\{file_name}')
        with open(path, 'r', encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=',')
            return list(reader)

    def handle(self, *args, **options):
        data = self.csv_to_dict('users.csv')
        for row in data:
            form = MyUserForm(data=row)
            form.save()

        data = self.csv_to_dict('category.csv')
        for row in data:
            form = CategoryForm(data=row)
            form.save()

        data = self.csv_to_dict('genre.csv')
        for row in data:
            form = GenreForm(data=row)
            form.save()

        data = self.csv_to_dict('review.csv')
        for row in data:
            form = ReviewForm(data=row)
            form.save()

        data = self.csv_to_dict('titles.csv')
        for row in data:
            form = TitleForm(data=row)
            form.save()

        data = self.csv_to_dict('comments.csv')
        for row in data:
            form = CommentForm(data=row)
            form.save()

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

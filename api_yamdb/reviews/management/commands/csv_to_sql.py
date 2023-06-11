import csv
import os

from django.core.management.base import BaseCommand  # CommandError

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
        'genre_title.csv',
    )

    def csv_to_dict(self, file_name):
        path = os.path.realpath(f'.\\api_yamdb\\static\\data\\{file_name}')
        with open(path, 'r', encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=',')
            return list(reader)

    def main(self):
        data = self.csv_to_dict('users.csv')
        for row in data:
            if row[0] != 'id':
                form = MyUserForm(data=row)
                form.save()

        data = self.csv_to_dict('category.csv')
        for row in data:
            if row[0] != 'id':
                form = CategoryForm(data=row)
                form.save()

        data = self.csv_to_dict('genre.csv')
        for row in data:
            if row[0] != 'id':
                form = GenreForm(data=row)
                form.save()

        data = self.csv_to_dict('review.csv')
        for row in data:
            if row[0] != 'id':
                form = ReviewForm(data=row)
                form.save()

        data = self.csv_to_dict('titles.csv')
        for row in data:
            if row[0] != 'id':
                form = TitleForm(data=row)
                form.save()

        data = self.csv_to_dict('comments.csv')
        for row in data:
            if row[0] != 'id':
                form = CommentForm(data=row)
                form.save()

        data = self.csv_to_dict('genre_title.csv')
        for row in data:
            if row[0] != 'id':
                ...

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



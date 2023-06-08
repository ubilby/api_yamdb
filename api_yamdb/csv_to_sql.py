import os
import csv
import sqlite3


def csv_to_dict(file_name):
    cur_path = os.path.dirname(__file__)
    print(cur_path)
    new_path = os.path.realpath(f'.\\api_yamdb\\static\\data\\{file_name}')
    print(new_path)
    with open(new_path, 'r', encoding="utf-8") as read_obj:
        data = csv.DictReader(read_obj, delimiter=',')
        return list(data)


def main():
    con = sqlite3.connect('api_yamdb/db.sqlite3')
    cur = con.cursor
    data = csv_to_dict('users.csv')
    for dict_list in data:
        cur.execute(
            "INSERT INTO reviews_customuser VALUES "
            " (:id, '', '', '', :email, :username, :first_name, "
            " :last_name, '', :bio, '', :role)",
            dict_list
        )
    data = csv_to_dict('genre.csv')
    for dict_list in data:
        cur.execute(
            "INSERT INTO reviews_genre VALUES (:id, :name, :slug)",
            dict_list
        )
    data = csv_to_dict('category.csv')
    for dict_list in data:
        cur.execute(
            "INSERT INTO reviews_category VALUES (:id, :name, :slug)",
            dict_list
        )
    data = csv_to_dict('titles.csv')
    for dict_list in data:
        cur.execute(
            "INSERT INTO reviews_titles VALUES "
            "(:id, :name, :year, '', :category)",
            dict_list
        )
    data = csv_to_dict('genre_title.csv')
    for dict_list in data:
        cur.execute(
            "INSERT INTO reviews_titlegenre VALUES "
            "(:id, :genre_id, :title_id)",
            dict_list
        )
    data = csv_to_dict('review.csv')
    for dict_list in data:
        cur.execute(
            "INSERT INTO reviews_category VALUES "
            "(:id, :text, :score, :pub_date, :author, :review_id)",
            dict_list
        )
    data = csv_to_dict('comments.csv')
    for dict_list in data:
        cur.execute(
            "INSERT INTO reviews_comments VALUES "
            "(:id, :text, :pub_date, :author, :review_id)",
            dict_list
        )
    con.commit()

from django.contrib import admin

from .models import Category, Genre, MyUser, Title

admin.site.register([Category, Genre, MyUser, Title])

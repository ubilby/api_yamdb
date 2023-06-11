from django.forms import ModelForm

from .models import Category, Comment, Genre, MyUser, Review, Title


class TitleForm(ModelForm):
    class Meta:
        model = Title
        fields = ('__all__')


class MyUserForm(ModelForm):
    class Meta:
        model = MyUser
        fields = (
            'id',
            'username',
            'email',
            'role',
            'first_name',
            'last_name',
        )


class GenreForm(ModelForm):
    class Meta:
        model = Genre
        fields = ('__all__')


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ('__all__')


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ('__all__')


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('__all__')

import re
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(creation_year):
    if creation_year > timezone.now().year:
        raise ValidationError(
            f'Год не может быть больше {timezone.now().year}'
        )


def username_validator(value):
    pattern = r'^[\w.@+-]+\Z'
    if re.match(pattern, value) is None:
        raise ValidationError(
            'Имя пользователя содержит недопустимые символы.'
        )

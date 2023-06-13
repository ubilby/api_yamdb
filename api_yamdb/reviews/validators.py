import re

from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(creation_year):
    if creation_year > timezone.now().year:
        raise ValidationError(
            f'Год не может быть больше {timezone.now().year}'
        )


def username_validator(value):
    unmatched = re.sub(r'^[\w.@+-]+\Z', '', value)
    if value == "me":
        raise ValidationError('Имя пользователя "me" использовать нельзя!')
    elif value in unmatched:
        raise ValidationError(
            f"Имя пользователя не должно содержать {unmatched}"
        )
    return value

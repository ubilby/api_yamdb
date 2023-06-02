from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(creation_year):
    now = timezone.now().year
    if creation_year > now:
        raise ValidationError(
            f'{creation_year} не может быть больше {now}'
        )

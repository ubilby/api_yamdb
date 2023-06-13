import re

from django.core.exceptions import ValidationError


def is_valid_role(role):
    valid_roles = ['admin', 'user', 'moderator']
    return role in valid_roles

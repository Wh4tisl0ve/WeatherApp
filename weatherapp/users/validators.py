import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_latin_and_num(validating_str: str):
    if not re.match(r'^[a-zA-Z0-9\-$]+$', validating_str):
        raise ValidationError(_('Поля могут содержать только латинские буквы, цифры и знаки:- и $'))

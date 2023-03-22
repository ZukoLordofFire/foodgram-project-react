from django.core.exceptions import ValidationError


def validate_amount(value):
    if value < 1:
        return value
    raise ValidationError(
        'Количество не может быть меньше 1')

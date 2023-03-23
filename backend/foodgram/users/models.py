from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import validate_username


class UserRole(models.TextChoices):
    """Роли пользователей."""
    USER = 'user'
    ADMIN = 'admin'


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True,
                                validators=[validate_username])
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150, unique=False)
    second_name = models.CharField(max_length=150, unique=False)
    role = models.CharField(
        max_length=10,
        help_text='роль пользователя в системе',
        choices=UserRole.choices,
        default=UserRole.USER
    )
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

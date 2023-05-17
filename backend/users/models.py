from django.contrib.auth.models import AbstractUser
from django.db import models
from users.validators import validate_username


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True,
                                validators=[validate_username])
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = models.CharField(max_length=64)
    is_active = models.BooleanField(
        verbose_name='Активен',
        default=True,
    )
    LOGIN_FIELD = 'username'
    REQUIRED_FIELDS = ('email', 'first_name', 'last_name', 'password',)


class Follow(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='followed',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        verbose_name='Фолловер',
        related_name='follower',
        on_delete=models.CASCADE,
    )

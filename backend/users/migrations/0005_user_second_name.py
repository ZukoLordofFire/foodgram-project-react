# Generated by Django 3.2 on 2023-05-03 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_user_second_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='second_name',
            field=models.CharField(default='Test', max_length=150),
        ),
    ]

# Generated by Django 3.2 on 2023-05-13 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_user_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='second_name',
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=150),
        ),
    ]
# Generated by Django 3.2 on 2023-05-03 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20230503_1047'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favourite',
            options={'verbose_name': 'Объект избранного', 'verbose_name_plural': 'Объекты избранного'},
        ),
        migrations.RemoveField(
            model_name='favourite',
            name='date_added',
        ),
        migrations.AddConstraint(
            model_name='favourite',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_favorite_user_recipe'),
        ),
    ]
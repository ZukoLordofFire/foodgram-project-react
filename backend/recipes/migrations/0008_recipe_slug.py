# Generated by Django 3.2 on 2023-05-03 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_auto_20230503_1227'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='slug',
            field=models.SlugField(default='meatwitheggs', verbose_name='Слаг'),
        ),
    ]
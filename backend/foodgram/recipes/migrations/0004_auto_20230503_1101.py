# Generated by Django 3.2 on 2023-05-03 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20230503_1052'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ingredients',
            new_name='Ingredient',
        ),
        migrations.RenameField(
            model_name='ingredientamount',
            old_name='ingredients',
            new_name='ingredient',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='ingredients',
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredient',
            field=models.ManyToManyField(related_name='recipe_ingredients', through='recipes.IngredientAmount', to='recipes.Ingredient', verbose_name='Необходимые ингридиенты'),
        ),
    ]
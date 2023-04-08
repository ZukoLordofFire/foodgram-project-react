# Generated by Django 3.2 on 2023-04-08 20:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор рецепта'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', through='recipes.IngredientAmount', to='recipes.Ingredients', verbose_name='Ингредиенты блюда'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', to='recipes.Tag', verbose_name='Тег'),
        ),
        migrations.AddConstraint(
            model_name='ingredients',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='unique_for_ingredient'),
        ),
        migrations.AddConstraint(
            model_name='ingredients',
            constraint=models.CheckConstraint(check=models.Q(name__length__gt=0), name='\nrecipes_ingredients_name is empty\n'),
        ),
        migrations.AddConstraint(
            model_name='ingredients',
            constraint=models.CheckConstraint(check=models.Q(measurement_unit__length__gt=0), name='\nrecipes_ingredients_measurement_unit is empty\n'),
        ),
        migrations.AddField(
            model_name='ingredientamount',
            name='ingredients',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe', to='recipes.ingredients', verbose_name='Связанные ингредиенты'),
        ),
        migrations.AddField(
            model_name='ingredientamount',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient', to='recipes.recipe', verbose_name='В каких рецептах'),
        ),
        migrations.AddField(
            model_name='favourite',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_favorites', to='recipes.recipe', verbose_name='Понравившиеся рецепты'),
        ),
        migrations.AddField(
            model_name='favourite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='cart',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_carts', to='recipes.recipe', verbose_name='Рецепты в списке покупок'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carts', to=settings.AUTH_USER_MODEL, verbose_name='Владелец списка'),
        ),
        migrations.AddConstraint(
            model_name='recipe',
            constraint=models.UniqueConstraint(fields=('name', 'author'), name='unique_for_author'),
        ),
        migrations.AddConstraint(
            model_name='recipe',
            constraint=models.CheckConstraint(check=models.Q(name__length__gt=0), name='\nrecipes_recipe_name is empty\n'),
        ),
        migrations.AddConstraint(
            model_name='ingredientamount',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredients'), name='\nrecipes_ingredientamount ingredient alredy added\n'),
        ),
        migrations.AddConstraint(
            model_name='favourite',
            constraint=models.UniqueConstraint(fields=('recipe', 'user'), name='\nrecipes_favourite recipe is favorite alredy\n'),
        ),
        migrations.AddConstraint(
            model_name='cart',
            constraint=models.UniqueConstraint(fields=('recipe', 'user'), name='\nrecipes_cart recipe is cart alredy\n'),
        ),
    ]

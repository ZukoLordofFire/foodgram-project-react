# Generated by Django 3.2 on 2023-05-19 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_auto_20230518_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientamount',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_ingredientts', to='recipes.recipe', verbose_name='Рецепт'),
        ),
    ]
from django.contrib.auth import get_user_model
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Тег',
        max_length=56,
        unique=True,
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        unique=True,
        validators=[RegexValidator(regex=r'#[A-Fa-f0-9]{6}')],
    )
    slug = models.CharField(
        verbose_name='Слаг',
        max_length=56,
        unique=True,
        validators=[RegexValidator(regex=r'[A-Za-z0-9_-]+')],
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Ингредиент',
        max_length=56,
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=64,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class Recipe(models.Model):
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=56,
    )
    author = models.ForeignKey(User,
                               verbose_name='Автор рецепта',
                               related_name='recipe_author',
                               on_delete=models.SET_NULL,
                               null=True,
                               )
    tags = models.ManyToManyField(Tag,
                                  verbose_name='Тег',
                                  related_name='recipe_tag',
                                  )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Необходимые ингридиенты',
        related_name='recipe_ingredients',
        through='IngredientAmount',
        through_fields=('recipe', 'ingredient')
    )
    slug = models.SlugField(verbose_name='Слаг')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    image = models.ImageField(
        verbose_name='Изображение блюда',
        upload_to='recipe_images/',
    )
    text = models.TextField(
        verbose_name='Описание блюда',
        max_length=300,
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=(
            MinValueValidator(
                0,
                'Время готовки не может быть равным 0',
            ),
            MaxValueValidator(
                10080,
                'Люди столько не живут',
            ),
        ),
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date', )


class Favourite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Понравившиеся рецепты',
        related_name='in_favourites',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='favourites',
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite_user_recipe'
            )
        ]
        verbose_name = 'Объект избранного'
        verbose_name_plural = 'Объекты избранного'


class Cart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепты в списке покупок',
        related_name='in_carts',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        verbose_name='Владелец списка',
        related_name='cart_owner',
        on_delete=models.CASCADE,
    )
    date_added = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Рецепт в списке покупок'
        verbose_name_plural = 'Рецепты в списке покупок'


class IngredientAmount(models.Model):
    amount = models.PositiveIntegerField(
        verbose_name='Количество'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipe_ingredientts'
    )

    def __str__(self):
        return f'{self.ingredient} в {self.recipe}'

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'

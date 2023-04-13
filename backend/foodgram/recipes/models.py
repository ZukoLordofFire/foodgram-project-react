from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
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
    )
    slug = models.CharField(
        verbose_name='Слаг',
        max_length=56,
        unique=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)


class Ingredients(models.Model):
    name = models.CharField(
        verbose_name='Ингридиент',
        max_length=56,
    )
    measurement = models.CharField(
        verbose_name='Единицы измерения',
        max_length=64,
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        ordering = ('name', )


class Recipe(models.Model):
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=56,
    )
    author = models.ForeignKey(User,
        verbose_name='Автор рецепта',
        related_name='recipes',
        on_delete=models.SET_NULL,
        null=True,
    )
    tags = models.ManyToManyField(Tag,
        verbose_name='Тег',
        related_name='recipes',
    )
    ingredients = models.ManyToManyField(Ingredients,
        verbose_name='Необходимые ингридиенты',
        related_name='recipes',
        through='recipes.IngredientAmount',
    )
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
        default=0,
        validators=(
            MinValueValidator(0,
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
    recipe = models.ForeignKey(Recipe,
        verbose_name='Понравившиеся рецепты',
        related_name='in_favourites',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(User,
        verbose_name='Пользователь',
        related_name='favourites',
        on_delete=models.CASCADE,
    )
    date_added = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'


class Cart(models.Model):
    recipe = models.ForeignKey(Recipe,
        verbose_name='Рецепты в списке покупок',
        related_name='in_carts',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(User,
        verbose_name='Владелец списка',
        related_name='carts',
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
    recipe = models.ForeignKey(Recipe,
        verbose_name='В каких рецептах',
        related_name='ingredient',
        on_delete=models.CASCADE,
    )
    ingredients = models.ForeignKey(Ingredients,
        verbose_name='Связанные ингредиенты',
        related_name='recipe',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        default=0,
        validators=(
            MinValueValidator(0,
                'Вы не можете положить 0',
            ),
            MaxValueValidator(
                100,
                'Слишком много, попробуйте воспользоваться другими единицами измерения',
            ),
        ),
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Количество ингридиентов'
        ordering = ('recipe', )


class Follow(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='follower',
                             verbose_name='Последователь')
    following = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  related_name='following',
                                  verbose_name='Последуемый')

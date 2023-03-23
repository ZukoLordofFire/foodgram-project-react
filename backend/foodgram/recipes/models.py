from django.db import models
from django.contrib.auth import get_user_model

from recipes.validators import validate_amount

User = get_user_model()


UNITS_CHOICES = (
    ("1", "г."),
    ("2", "мл"),
    ("3", "шт"),
    ("4", "ст. л."),
    ("5", "по вкусу"),
    ("6", "щепотка"),
    ("7", "ч. л."),
    ("8", "стакан"),
    ("9", "капля"),
    ("10", "бутылка"),
    ("11", "кг"),
    ("12", "лист"),
    ("13", "головка"),
    ("14", "зубчик"),
    ("15", "пучок"),
    ("16", "кусок"),
    ("17", "кубик"),
    ("18", "на глаз"),
    ("19", "долька"),
    ("20", "веточка"),
    ("21", "горсть"),
    ("22", "пакет"),
    ("23", "банка"),
    ("24", "упаковка"),
    ("25", "миска"),
    ("26", "кружка"),
)

INGRIDIENTS_CHOICES = ()


class Recipe_Tag(models.Model):
    BLUE = '#0000FF'
    ORANGE = '#FFA500'
    GREEN = '#008000'
    PURPLE = '#800080'
    YELLOW = '#FFFF00'

    COLOR_CHOICES = [
        (BLUE, 'Синий'),
        (ORANGE, 'Оранжевый'),
        (GREEN, 'Зеленый'),
        (PURPLE, 'Фиолетовый'),
        (YELLOW, 'Желтый'),
    ]
    tag_name = models.CharField(unique=True, max_length=150)
    tag_slug = models.SlugField(unique=True)
    HEX_code = models.CharField(unique=True, choices=COLOR_CHOICES,
                                max_length=10)


class Ingridients(models.Model):
    name = models.CharField(max_length=150)
    amount = models.IntegerField
    measurement_unit = models.CharField(choices=UNITS_CHOICES, max_length=150)


class Recipe(models.Model):
    recipe_name = models.CharField('Название рецепта',
                                   help_text='Введите название',
                                   max_length=150)
    text = models.TextField('Текстовое описание',
                            help_text='Введите текст')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    ingridients = models.ManyToManyField(Ingridients)
    recipe_tag = models.ManyToManyField(Recipe_Tag)
    SIX_ACTS = 6
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор')
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/',
        blank=True
    )
    coocking_duration = models.IntegerField('Время приготовления')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='follower',
                             verbose_name='Последователь')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='following',
                               verbose_name='Последуемый')


class Favourite(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='Пользователь')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='favourite_recipe',
                               verbose_name='Избранный рецепт')


class Cart(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='cart',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='cart',
                               verbose_name='Рецепт')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Список покупок'


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(Ingridients,
                                   on_delete=models.CASCADE,
                                   verbose_name='Ингридиент')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт')
    amount = models.IntegerField(validators=[validate_amount])

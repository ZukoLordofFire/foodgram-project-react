from __future__ import annotations

from typing import TYPE_CHECKING

from recipes.models import IngredientAmount, Recipe

if TYPE_CHECKING:
    from recipes.models import Ingredients


def recipe_ingredients_set(
    recipe: Recipe,
    ingredients: dict[int, tuple['Ingredients', int]]
) -> None:
    objs = []

    for ingredient, amount in ingredients.values():
        objs.append(IngredientAmount(
            recipe=recipe,
            ingredients=ingredient,
            amount=amount
        ))

    IngredientAmount.objects.bulk_create(objs)


incorrect_layout = str.maketrans(
    'qwertyuiop[]asdfghjkl;\'zxcvbnm,./',
    'йцукенгшщзхъфывапролджэячсмитьбю.'
)

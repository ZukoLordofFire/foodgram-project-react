from django.contrib.auth import get_user_model
from django import forms

from .models import Recipe


User = get_user_model()


# доработать
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('recipe_name', 'text', 'image', 'cooking_duration')
        labels = {
            'text': 'Текст рецепта',
            'recipe_name': 'Название рецепта',
            'image': 'Картинка рецепта',
            'cooking_duration': 'Время приготовления',
        }

        def not_empty_field(self):
            data = self.cleaned_data['text']
            if data == '':
                raise forms.ValidationError(
                    'Поле не должно оставаться пустым!'
                )
            return data

from django.contrib.auth import get_user_model
from django import forms

from .models import Recipe


User = get_user_model()


# доработать
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('recipe_name', 'text', 'image', )
        labels = {
            'text': 'Текст поста',
            'group': 'Сообщество',
        }

        def not_empty_field(self):
            data = self.cleaned_data['text']
            if data == '':
                raise forms.ValidationError(
                    'Поле не должно оставаться пустым!'
                )
            return data

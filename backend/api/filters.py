import django_filters
from django.contrib.auth import get_user_model
from recipes.models import Recipe
from rest_framework.filters import SearchFilter

User = get_user_model


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'


class AuthorAndTagFilter(django_filters.FilterSet):
    tags = django_filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = django_filters.ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Recipe
        fields = ('tags', 'author')

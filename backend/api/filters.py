import django_filters
from recipes.models import Recipe, Tag
from rest_framework.filters import SearchFilter


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'


class AuthorAndTagFilter(django_filters.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all(),
                                                    field_name="tags__slug",
                                                    to_field_name="slug",)

    class Meta:
        model = Recipe
        fields = ('tags',)

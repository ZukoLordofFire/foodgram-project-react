import django_filters
from django.contrib.auth import get_user_model
from recipes.models import Recipe, Tag
from rest_framework.filters import SearchFilter

User = get_user_model


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'


class AuthorAndTagFilter(django_filters.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all())
    is_favorited = django_filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = django_filters.BooleanFilter(
        method='filter_is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(in_favourites__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(in_carts__user=user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('tags',)

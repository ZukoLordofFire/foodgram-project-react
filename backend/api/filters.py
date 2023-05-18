import django_filters
from django.contrib.auth import get_user_model
from recipes.models import Recipe
from rest_framework.filters import SearchFilter

User = get_user_model()


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.Filter(method='filter_tag')
    is_favorited = django_filters.Filter(method='filter_is_favorited')
    is_in_shopping_cart = django_filters.Filter(
        method='filter_is_in_shopping_cart')
    author = django_filters.NumberFilter(field_name='author_id',
                                         lookup_expr='exact')

    class Meta:
        model = Recipe
        fields = ('tags', 'is_favorited', 'is_in_shopping_cart', 'author')

    def filter_tag(self, queryset, name, value):
        tags = self.data.getlist('tags')
        if value == '0':
            return queryset
        return queryset.filter(tags__slug__in=tags).distinct()

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

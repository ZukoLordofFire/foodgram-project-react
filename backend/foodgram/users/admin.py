from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from recipes.models import (Cart, Favourite, Ingredient, IngredientAmount,
                            Recipe, Tag)
from users.models import Follow, User


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'second_name',
            'password',
        )


class TagResource(resources.ModelResource):

    class Meta:
        model = Tag
        fields = (
            'color',
            'name',
            'slug',
        )


class IngredientAmountResource(resources.ModelResource):

    class Meta:
        model = IngredientAmount
        fields = (
            'recipe',
            'ingredient',
            'amount',
        )


@admin.register(IngredientAmount)
class IngredientAmountAdmin(ImportExportModelAdmin):
    resource_classes = [IngredientAmountResource]
    list_display = (
            'recipe',
            'ingredient',
            'amount',
    )


class CartResource(resources.ModelResource):

    class Meta:
        model = Cart
        fields = (
            'recipe',
            'user',
            'date_added',
        )


@admin.register(Cart)
class CartAdmin(ImportExportModelAdmin):
    resource_classes = [CartResource]
    list_display = (
            'recipe',
            'user',
            'date_added',
    )


@admin.register(Tag)
class TagAdmin(ImportExportModelAdmin):
    resource_classes = [TagResource]
    list_display = (
        'color',
        'name',
        'slug',
    )


class RecipeResource(resources.ModelResource):

    class Meta:
        model = Recipe
        fields = (
            'name',
            'author',
            'tags',
            'ingredients',
            'slug',
            'pub_date',
            'image',
            'text',
            'cooking_time',
        )


@admin.register(Recipe)
class RecipeAdmin(ImportExportModelAdmin):
    resource_classes = [RecipeResource]
    list_display = (
        'name',
        'author',
        'slug',
        'pub_date',
        'image',
        'text',
        'cooking_time',
    )
    list_filter = ('name', 'author', 'tags')

    def get_favourite_count(self, obj):
        return Favourite.objects.filter(recipe=obj).count()
    get_favourite_count.short_description = 'Избранное'


class IngredientResource(resources.ModelResource):

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


@admin.register(Ingredient)
class IngredientsAdmin(ImportExportModelAdmin):
    resource_classes = [IngredientResource]
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    list_filter = ('name',)


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    resource_classes = [UserResource]
    list_display = (
        'username',
        'email',
        'first_name',
        'second_name',
        'password',
    )
    list_filter = ('username', 'email')


class FollowResource(resources.ModelResource):

    class Meta:
        model = Follow
        firleds = (
            'author',
            'user',
        )


@admin.register(Follow)
class FollowAdmin(ImportExportModelAdmin):
    resource_classes = [FollowResource]
    list_display = (
            'author',
            'user',
    )

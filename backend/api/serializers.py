from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Cart, Favourite, Ingredient, IngredientAmount,
                            Recipe, Tag)
from rest_framework import serializers
from users.models import Follow

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('__all__',)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = ('__all__',)


class IngredientsinRecipeSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(
        source='ingredient.name'
    )
    measurement_unit = serializers.StringRelatedField(
        source='ingredient.measurement_unit'
    )
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = IngredientAmount
        fields = ('amount', 'name', 'measurement_unit', 'id')


class RecipeListSerializer(serializers.ModelSerializer):

    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited',
        read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart',
        read_only=True)
    image = Base64ImageField()

    def get_ingredients(self, obj):
        return IngredientsinRecipeSerializer(
            IngredientAmount.objects.filter(recipe=obj).all(), many=True
        ).data

    class Meta:
        model = Recipe
        fields = (
            'name',
            'ingredients',
            'is_favorited',
            'text',
            'is_in_shopping_cart',
            'image',
            'author',
            'tags',
            'id',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user

        if user.is_anonymous:
            return False

        return Favourite.objects.filter(user=user, recipe=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user

        if user.is_anonymous:
            return False

        return Cart.objects.filter(user=user, recipe=obj.id).exists()


class IngredientCreateInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    ingredients = IngredientCreateInRecipeSerializer(many=True)

    def validate_ingredients(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("Добавьте хотя бы один.")
        return value

    def create(self, data):
        ingredients = data.pop('ingredients')
        recipe = Recipe.objects.create(**data,
                                       author=self.context['request'].user)

        create_ingredients = [
            IngredientAmount(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            )
            for ingredient in ingredients
        ]
        IngredientAmount.objects.bulk_create(
            create_ingredients
        )
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        if ingredients is not None:
            instance.ingredients.clear()

            create_ingredients = [
                IngredientAmount(
                    recipe=instance,
                    ingredient=ingredient['id'],
                    amount=ingredient['amount']
                )
                for ingredient in ingredients
            ]
            IngredientAmount.objects.bulk_create(
                create_ingredients
            )
        return super().update(instance, validated_data)

    class Meta:
        model = Recipe
        fields = ('name', 'ingredients', 'text', 'cooking_time')

    def to_representation(self, obj):
        self.fields.pop('ingredients')
        representation = super().to_representation(obj)
        representation['ingredients'] = IngredientsinRecipeSerializer(
            IngredientAmount.objects.filter(recipe=obj).all(),
            many=True
        ).data
        return representation

    class Meta:
        model = Recipe
        fields = ('name', 'ingredients', 'text')


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id',
                  'email',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed')
        read_only_fields = 'is_subscribed',

    def get_is_subscribed(self, obj):
        user = self.context.get('request')
        return Follow.objects.filter(user=user, author=obj.id).exists()


class FollowSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'is_subscribed',
            'first_name',
            'last_name',
            'recipes',
            'recipes_count',
        )
        read_only_fields = '__all__',

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj)
        return RecipeListSerializer(queryset, many=True).data

    def get_is_subscribed(*args):
        return True

    def get_recipes_count(self, user):
        return Recipe.objects.filter(author=user).count()

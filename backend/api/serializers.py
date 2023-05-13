from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Cart, Favourite, Ingredient, IngredientAmount,
                            Recipe, Tag)
from rest_framework import serializers

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
        source='ingredient',
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = IngredientAmount
        fields = ('amount', 'name', 'measurement_unit', 'id')


class RecipeListSerializer(serializers.ModelSerializer):

    ingredients = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField(
        method_name='get_is_favorite',
        read_only=True)
    is_in_cart = serializers.SerializerMethodField(
        method_name='get_is_in_cart',
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
            'is_favorite',
            'text',
            'is_in_cart',
            'image',
        )

    def get_is_favorite(self, obj):
        user = self.context.get('request').user

        if user.is_anonymous:
            return False

        return Favourite.objects.filter(user=user, recipe=obj.id).exists()

    def get_is_in_cart(self, obj):
        user = self.context.get('request').user

        if user.is_anonymous:
            return False

        return Cart.objects.filter(user=user, recipe=obj.id).exists()


class IngredientCreateInRecipeSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(read_only=True)
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField(write_only=True, min_value=1)

    class Meta:
        model = IngredientAmount
        fields = ('recipe', 'id', 'amount')


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    ingredients = IngredientCreateInRecipeSerializer(many=True)

    def validate_ingredients(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("Добавьте хотя бы один.")
        return value

    def create(self, data):
        ingredients = data.pop('ingredients')
        recipe = Recipe.objects.create(**data)

        create_ingredients = [
            IngredientAmount(
                recipe=recipe,
                ingredient=ingredient['ingredient'],
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
                    ingredient=ingredient['ingredient'],
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
        fields = ('name', 'ingredients', 'text')


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',
                  'email',
                  'username',
                  'first_name',
                  'last_name',
                  'is_following')
        read_only_fields = 'is_following',


class CustomUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id',
                  'email',
                  'username',
                  'first_name',
                  'second_name',
                  'password',
                  'is_following')

    def create(self, data):
        password = data.pop('password', None)
        instance = self.Meta.model(**data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class FollowSerializer(serializers.ModelSerializer):
    recipes = RecipeListSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'is_following',
            'first_name',
            'second_name',
            'recipes',
            'recipes_count',
        )
        read_only_fields = '__all__',

    def get_is_following(*args):
        return True

    def get_recipes_count(self, user):
        return user.recipes.count()

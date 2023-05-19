from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Ingredient, IngredientAmount, Recipe, Tag
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
    id = serializers.IntegerField(source='ingredient.id')

    class Meta:
        model = IngredientAmount
        fields = ('amount', 'name', 'measurement_unit', 'id')


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
        user = self.context['request'].user
        if user.is_anonymous or obj == user:
            return False
        return Follow.objects.filter(user=user, author=obj.id).exists()


class RecipeListSerializer(serializers.ModelSerializer):

    ingredients = IngredientsinRecipeSerializer(many=True,
                                                source='recipe_ingredientts')
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited',
        read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart',
        read_only=True)
    image = Base64ImageField()
    tags = TagSerializer(many=True)
    author = CustomUserSerializer()

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
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Recipe.objects.filter(
            in_favourites__user=request.user, id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Recipe.objects.filter(
            in_carts__user=request.user, id=obj.id).exists()


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
    image = Base64ImageField()
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )

    class Meta:
        model = Recipe
        fields = ('name',
                  'ingredients', 'text', 'cooking_time', 'image', 'tags')

    def validate_ingredients(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("Добавьте хотя бы один.")
        return value

    def create(self, data):
        ingredients = data.pop('ingredients')
        tags = data.pop('tags')
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
        recipe.tags.set(tags)
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

    def to_representation(self, obj):
        return RecipeListSerializer(obj, context=self.context).data


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
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        if limit:
            queryset = queryset[:int(limit)]
        return ShortRecipeSerializer(queryset, many=True).data

    def get_is_subscribed(*args):
        return True

    def get_recipes_count(self, user):
        return Recipe.objects.filter(author=user).count()


class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'cooking_time',
            'image',
        )


class SubscribtionsSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'last_name',
            'first_name',
            'id',
            'username',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, obj):
        return True

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj)
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        if limit:
            queryset = queryset[:int(limit)]
        return ShortRecipeSerializer(queryset, many=True).data

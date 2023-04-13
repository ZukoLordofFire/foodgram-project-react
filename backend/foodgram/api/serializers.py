from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import F, QuerySet
from django.db.transaction import atomic
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from core.services import recipe_ingredients_set
from core.validators import ingredients_validator, tags_exist_validator
from recipes.models import Ingredients, Recipe, Tag

User = get_user_model()

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = '__all__'
        read_only_fields = '__all__'


class ReadRecipeSerializer(serializers.ModelSerializer):
    Tag = TagSerializer
    class Meta:
        model = Recipe


class WriteRecipeSerializer(serializers.ModelSerializer):
    Tag = serializers.SlugRelatedField(QuerySet=Tag.objects.all, slug_field='slug')
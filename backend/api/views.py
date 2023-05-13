from io import BytesIO

from api.paginators import Pagination
from api.permissions import AdminOnly, CombinedPermission
from api.serializers import (CustomUserSerializer, FollowSerializer,
                             IngredientSerializer,
                             RecipeCreateUpdateSerializer,
                             RecipeListSerializer, TagSerializer)
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from recipes.models import (Cart, Favourite, Ingredient, IngredientAmount,
                            Recipe, Tag)
from reportlab.pdfgen import canvas
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from users.models import Follow

User = get_user_model()


class POSTandGETViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                        mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AdminOnly,)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AdminOnly,)


class RecipesViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    http_method_names = ['get', 'post', 'patch']
    permission_classes = (IsAuthenticated, CombinedPermission)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return RecipeCreateUpdateSerializer

        return RecipeListSerializer

    def get_queryset(self):
        recipes = Recipe.objects.all()

        author = self.request.query_params.get('author', None)
        if author:
            return recipes.filter(author=author)

        return recipes

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            if Favourite.objects.filter(user=self.request.user,
                                        recipe=recipe).exists():
                return Response(
                    {'message': 'Рецепт уже добавлен в избранное.'},
                    status=status.HTTP_400_BAD_REQUEST)
            Favourite.objects.create(user=self.request.user, recipe=recipe)
            return Response({'message': 'Рецепт успешно добавлен в избранное.'}
                            )
        if Favourite.objects.filter(user=self.request.user,
                                    recipe=recipe).exists():
            Favourite.objects.delete(user=self.request.user, recipe=recipe)
        return Response({'message': 'Рецепта нет в избранном.'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            if Cart.objects.filter(user=self.request.user,
                                   recipe=recipe).exists():
                return Response({'message': 'Рецепт уже добавлен в корзину.'},
                                status=status.HTTP_400_BAD_REQUEST)
            Cart.objects.create(user=self.request.user, recipe=recipe)
        if Cart.objects.filter(user=self.request.user, recipe=recipe).exists():
            Cart.objects.delete(user=self.request.user, recipe=recipe)
        return Response({'message': 'Рецепта нет в корзине.'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        user = self.request.user
        if not Cart.objects.filter(user=user).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ingredients = IngredientAmount.objects.filter(
            recipe__in_carts__user=request.user).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(
            ingredient_amount=Sum('amount'))

        buffer = BytesIO()
        pdf_list = canvas.Canvas(buffer)
        pdf_list.drawString(200, 750, 'Ваш список покупок')
        height = 700
        width = 100
        for i, item in enumerate(ingredients, 1):
            get_object_or_404(
                Recipe,
                ingredientamount__ingredient__name=item['ingredient__name'])
            pdf_list.drawString(width, height, (
                f'{i}. {item["ingredient__name"]} - '
                f'{item["ingredient_amount"]}, '
                f'{item["ingredient__measurement_unit"]}. '))
            height -= 25
        pdf_list.showPage()
        pdf_list.save()
        buffer.seek(0)
        return FileResponse(
            buffer,
            as_attachment=True,
            filename='to_buy_list.pdf'
        )


class UserViewSet(POSTandGETViewSet):
    queryset = User.objects.all()
    pagination_class = Pagination
    serializer_class = FollowSerializer

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = CustomUserSerializer(context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        queryset = Follow.objects.filter(user=self.request.user)
        if self.request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(pages, many=True)
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, id):
        if request.method == 'POST':
            if Follow.objects.filter(request.user, author__id=id).exists():
                return Response({'message': 'Вы уже подписаны на автора.'},
                                status=status.HTTP_400_BAD_REQUEST)
            Follow.objects.create(request.user, author__id=id)
        if Follow.objects.filter(request.user, author__id=id).exists():
            Follow.objects.delete(request.user, author__id=id)
        return Response({'message': 'Вы не подписаны на этого автора'},
                        status=status.HTTP_400_BAD_REQUEST)

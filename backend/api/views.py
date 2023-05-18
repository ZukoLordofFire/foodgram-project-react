from api.filters import AuthorAndTagFilter, IngredientSearchFilter
from api.paginators import Pagination
from api.permissions import AdminOnly, CombinedPermission
from api.serializers import (CustomUserSerializer, IngredientSerializer,
                             RecipeCreateUpdateSerializer,
                             RecipeListSerializer, SubscribtionsSerializer,
                             TagSerializer)
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import (Cart, Favourite, Ingredient, IngredientAmount,
                            Recipe, Tag)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
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
    filter_backends = [IngredientSearchFilter]
    search_fields = ['name']


class RecipesViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    filterset_class = AuthorAndTagFilter
    filter_backends = [DjangoFilterBackend]
    pagination_class = Pagination
    permission_classes = (CombinedPermission,)

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
    def favorite(self, request, pk=None):
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
            Favourite.objects.filter(user=self.request.user,
                                     recipe=recipe).delete()
            return Response({'message': 'Рецепт больше не в избранном!'},
                            status=status.HTTP_204_NO_CONTENT)
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
            return Response({'message': 'Рецепт добавлен в корзину!'},
                            status=status.HTTP_201_CREATED)
        if Cart.objects.filter(user=self.request.user, recipe=recipe).exists():
            Cart.objects.filter(user=self.request.user, recipe=recipe).delete()
            return Response({'message': 'Рецепт убран из корзины!'},
                            status=status.HTTP_204_NO_CONTENT)
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

        pdfmetrics.registerFont(TTFont('TimesNewRoman', 'times.ttf'))
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="список_покупок.pdf"')
        p = canvas.Canvas(response)
        p.setFont("TimesNewRoman", 16)
        p.drawString(100, 700, "Список покупок")
        p.setFont("TimesNewRoman", 12)
        y = 650
        for ingredient in ingredients:
            name = ingredient['ingredient__name']
            measurement_unit = ingredient['ingredient__measurement_unit']
            amount = ingredient['ingredient_amount']
            p.drawString(100, y, f"{name} ({measurement_unit}): {amount}")
            y -= 20
        p.showPage()
        p.save()
        return response


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    pagination_class = Pagination
    serializer_class = CustomUserSerializer

    @action(['GET'], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, id):
        author = get_object_or_404(User, pk=id)
        if request.method == 'POST':
            if Follow.objects.filter(user=request.user,
                                     author=author).exists():
                return Response({'message': 'Вы уже подписаны на автора.'},
                                status=status.HTTP_400_BAD_REQUEST)
            Follow.objects.create(user=request.user, author=author)
            return Response({'message': 'Подписка усчпешна!'},
                            status=status.HTTP_201_CREATED)
        if Follow.objects.filter(user=request.user, author=author).exists():
            Follow.objects.filter(user=request.user, author=author).delete()
            return Response({'message': 'Подписка отменена!'},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'Вы не подписаны на этого автора'},
                        status=status.HTTP_400_BAD_REQUEST)


class SubscribtionsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = (IsAuthenticated, )
    serializer_class = SubscribtionsSerializer
    pagination_class = Pagination

    def get_queryset(self):
        return User.objects.filter(followed__user=self.request.user)

from api.views import (IngredientViewSet, RecipesViewSet, SubscribtionsViewSet,
                       TagViewSet, UserViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register('tags', TagViewSet, 'tags')
router.register('ingredients', IngredientViewSet, 'ingredients')
router.register('recipes', RecipesViewSet, 'recipes')
router.register('users/subscriptions', SubscribtionsViewSet, 'subscriptions')
router.register('users', UserViewSet, 'users')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

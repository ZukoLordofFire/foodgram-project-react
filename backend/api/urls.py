from api.views import (IngredientViewSet, RecipesViewSet, TagViewSet,
                       UserViewSet)
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register('tags', TagViewSet, 'tags')
router.register('ingredients', IngredientViewSet, 'ingredients')
router.register('recipes', RecipesViewSet, 'recipes')
router.register('users', UserViewSet, 'users')

urlpatterns = [
    path('auth/token/', obtain_auth_token),
    path('auth/', include('djoser.urls')),
    path('', include(router.urls)),
]

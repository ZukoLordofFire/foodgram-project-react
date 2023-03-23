from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path(
         'recipes/<int:recipe_id>/edit/',
         views.recipe_edit, name='update_recipe'),
    path(
         'recipes/<int:recipe_id>/',
         views.recipe_detail, name='recipe_detail'),
    path('create/', views.recipe_create, name='create_recipe'),
    path(
         'recipes/<int:recipe_id>/delete/',
         views.recipe_delete, name='recipe_delete'),
    path('recipes/follow_index/', views.follow_index, name='following'),
    path('recipes/favourites/', views.favourites, name='favourites'),
    path('recipes/cart/', views.your_cart, name='cart')

]

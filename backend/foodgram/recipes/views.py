from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .forms import RecipeForm
from .models import Recipe, User, Follow, Favourite, Cart


def index(request):
    template = 'recipes/index.html'
    title = 'Последние обновления на сайте'
    recipe_list = Recipe.objects.all().select_related('author',)
    paginator = Paginator(recipe_list, Recipe.SIX_ACTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': title,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    template = 'recipes/profile.html'
    author = get_object_or_404(User, username=username)
    recipes = author.recipes.all()
    paginator = Paginator(recipes, Recipe.SIX_ACTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.user.is_authenticated and Follow.objects.filter(
        author=author,
        user=request.user
    ).exists():
        following = True
    else:
        following = False
    context = {
        'page_obj': page_obj,
        'recipes': recipes,
        'author': author,
        'following': following
    }
    return render(request, template, context)


def recipe_detail(request, recipe_id):
    template = 'recipes/recipe_detail.html'
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    author = recipe.author
    context = {
        'recipe': recipe,
        'author': author,
    }
    return render(request, template, context)


@login_required
def recipe_create(request):
    template = 'recipes/create_recipe.html'
    form = RecipeForm(request.RECIPE or None,
                      files=request.FILES or None)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()
        return redirect('recipes:profile', request.user)
    return render(request, template, {'form': form})


@login_required
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    author = recipe.author
    if author != request.user:
        return redirect('recipes:recipe_detail', recipe_id)

    template = 'recipes/create_recipe.html'
    form = RecipeForm(request.RECIPE or None,
                      files=request.FILES or None,
                      instance=recipe)
    is_edit = True
    context = {
        'form': form,
        'is_edit': is_edit,
    }

    if form.is_valid():
        form.save()
        return redirect('recipes:recipe_detail', recipe_id)

    return render(request, template, context)



@login_required
def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    author = recipe.author
    if author != request.user:
        return redirect('recipes:recipe_detail', recipe_id)
    else:
        Recipe.objects.filter(recipe=recipe, author=author).delete()
    
    return redirect('recipe:index')
    

@login_required
def follow_index(request):
    title = 'Вы на них подписаны'
    template = 'recipes/follow.html'
    recipes = Recipe.objects.filter(author__following__user=request.user)
    paginator = Paginator(recipes, Recipe.SIX_ACTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'title': title,
    }
    return render(request, template, context)


@login_required
def favouries(request):
    title = 'Избранные рецепты'
    recipes = Recipe.objects.filter(recipe_favourite_user=request.user)
    template = 'recipes/favourites.html'
    paginator = Paginator(recipes, Recipe.SIX_ACTS)
    page_number = request.GET.page('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': title,
        'page_obj': page_obj
    }
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    template = 'recipes:profile'
    if (
            request.user == author
            or Follow.objects.get_or_create(
                author=author,
                user=request.user
            )
    ):
        return redirect(template, username=username)
    Follow.objects.create(author=author, user=request.user)

    return redirect(template, username=username)


@login_required
def recipe_favourite(request, recipe_id):
    recipe = Recipe.objects.filter(pk=recipe_id)
    template = 'recipes:detail'
    if (
            Favourite.objects.get_or_create(
                user=request.user,
                recipe=recipe
            )
    ):
        return redirect(template, pk=recipe_id)
    Favourite.objects.create(user=request.user, recipe=recipe)

    return redirect(template, pk=recipe_id)


@login_required
def add_cart(request, recipe_id):
    recipe = Recipe.objects.filter(pk=recipe_id)
    template = 'recipes:detail'
    if (
        Cart.objects.get_or_create(
            user=request.user,
            recipe=recipe
        )
    ):
        return redirect(template, pk=recipe_id)
    Cart.objects.create(user=request.user, recipe=recipe)

    return redirect(template, pk=recipe_id)


@login_required
def profile_unfollow(request, username):
    template = 'recipes:profile'
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(author=author, user=request.user).delete()
    return redirect(template, username=username)


@login_required
def recipe_unfavourite(request, recipe_id):
    template = 'recipes:detail'
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    Favourite.objects.filter(recipe=recipe, user=request.user).delete()
    return redirect(template, pk=recipe_id)


@login_required
def delete_cart(request, recipe_id):
    template = 'recipes:detail'
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    Cart.objects.filter(recipe=recipe, user=request.user).delete()
    return redirect(template, pk=recipe_id)


@login_required
def download_cart(request):
    template = 'recipes:cart'
    return redirect(template)

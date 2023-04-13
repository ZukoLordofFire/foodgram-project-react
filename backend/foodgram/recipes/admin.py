from __future__ import annotations

from django.contrib.admin import (ModelAdmin, TabularInline, display, register,
                                  site)
from django.core.handlers.wsgi import WSGIRequest
from django.utils.html import format_html
from django.utils.safestring import SafeString, mark_safe

from recipes.forms import TagForm
from recipes.models import (Cart, Favourite, IngredientAmount, Ingredients,
                            Recipe, Tag)

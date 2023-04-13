from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from users.models import User


class UserResource(resources.ModelResource):
    class Meta:
        model = User


@admin.register(User)
class RecipeAdmin(ImportExportModelAdmin):
    resource_classes = [UserResource]
    list_display = ('id', 'username', 'bio', 'role')

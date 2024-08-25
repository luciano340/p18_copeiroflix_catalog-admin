from django.contrib import admin
from django_project.apps.category.models import Category


class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
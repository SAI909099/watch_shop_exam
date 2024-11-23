from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.shops.models import Watches, Categories


@admin.register(Watches)
class Watches(ModelAdmin):
    pass
@admin.register(Categories)
class Categories(ModelAdmin):
    list_display = ('name',)



from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.shops.models import Watches, Categories, ImagesModel

from django.contrib import admin



class ImagesModelStackedInline(admin.StackedInline):
    model = ImagesModel
    extra = 0
    min_num = 1
    max_num = 8


@admin.register(Watches)
class ProductModelAdmin(admin.ModelAdmin):
    inlines = ImagesModelStackedInline,


@admin.register(Categories)
class Categories(ModelAdmin):
    list_display = ('name',)
#
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     pass


class WishlistAdmin(admin.ModelAdmin):
    pass

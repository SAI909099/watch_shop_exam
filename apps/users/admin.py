from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.shops.models import Product
from apps.users.models import User
from apps.users.forms import CustomAdminAuthenticationForm


@admin.register(Product)
class BookAdmin(admin.ModelAdmin):
    pass




admin.AdminSite.login_form = CustomAdminAuthenticationForm
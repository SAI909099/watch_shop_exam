from django.contrib import admin

from apps.users.forms import CustomAdminAuthenticationForm
from apps.users.models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass




admin.AdminSite.login_form = CustomAdminAuthenticationForm
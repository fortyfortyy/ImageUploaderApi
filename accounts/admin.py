from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.forms import CustomUserCreationForm
from accounts.models import AccountTier, UserAccount


class CustomUserAccountAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = UserAccount
    list_display = [
        "username",
        "account_tier",
        "email",
        "is_staff",
    ]
    list_display_links = ["username"]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("account_tier",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("account_tier",)}),)


admin.site.register(UserAccount, CustomUserAccountAdmin)
admin.site.register(AccountTier)

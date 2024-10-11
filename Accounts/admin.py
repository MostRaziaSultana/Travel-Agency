from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.



class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_vendor',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_vendor',)}),  # Add is_vendor field to add form
    )
    list_display = UserAdmin.list_display + ('is_vendor',)  # Optional: add to list view
    list_filter = UserAdmin.list_filter + ('is_vendor',)  # Optional: add filter


admin.site.register(CustomUser, CustomUserAdmin)
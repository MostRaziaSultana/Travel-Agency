from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Profile
# Register your models here.


#
# class CustomUserAdmin(UserAdmin):
#     fieldsets = UserAdmin.fieldsets + (
#         (None, {'fields': ('is_vendor',)}),
#     )
#     add_fieldsets = UserAdmin.add_fieldsets + (
#         (None, {'fields': ('is_vendor',)}),
#     )
#     list_display = UserAdmin.list_display + ('is_vendor',)
#     list_filter = UserAdmin.list_filter + ('is_vendor',)
#
#
# # admin.site.register(CustomUser, CustomUserAdmin)
#
# admin.site.register(Profile)
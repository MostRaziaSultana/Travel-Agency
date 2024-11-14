# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser,Profile
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




from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html

class CustomUserAdmin(UserAdmin):
    # Add 'Update' and 'Delete' fields in the user list display
    list_display = UserAdmin.list_display + ('update_link', 'delete_link')
    list_per_page = 20

    def update_link(self, obj):
        # Create an update link for each user
        update_url = reverse('admin:auth_user_change', args=[obj.pk])
        return format_html(
            '<a class="button" href="{}" style="color: white; background-color: green; padding: 5px 10px; border-radius: 5px; text-decoration: none;">Update</a>',
            update_url
        )

    update_link.short_description = 'Update'

    def delete_link(self, obj):
        # Create a delete link for each user
        delete_url = reverse('admin:auth_user_delete', args=[obj.pk])
        return format_html(
            '<a class="button" href="{}" style="color: white; background-color: red; padding: 5px 10px; border-radius: 5px; text-decoration: none;">Delete</a>',
            delete_url
        )

    delete_link.short_description = 'Delete'

# Unregister the existing User admin and register the customized one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
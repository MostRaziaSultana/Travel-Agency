from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.urls import reverse

# Register your models here.

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('address', 'mobile', 'hotline', 'email', 'support_mail', 'update_link', 'delete_link')
    search_fields = ('address', 'email', 'mobile', 'hotline')

    def update_link(self, obj):
        update_url = reverse('admin:Contact_contactus_change', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="color: white; background-color: green; padding: 5px 10px; border-radius: 5px;text-decoration: none;">Update</a>',
            update_url
        )
    update_link.short_description = 'Update'

    def delete_link(self, obj):
        delete_url = reverse('admin:Contact_contactus_delete', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="color: white; background-color: red; padding: 5px 10px; border-radius: 5px; text-decoration: none;">Delete</a>',
            delete_url
        )
    delete_link.short_description = 'Delete'


admin.site.register(ContactUs, ContactUsAdmin)

class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'email', 'mobile', 'created_at', 'seen', 'delete_link')
    search_fields = ('name', 'email', 'mobile')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        if obj and not obj.seen:
            obj.seen = True
            obj.save()  # Mark as seen
        return super(UserMessageAdmin, self).change_view(request, object_id, form_url, extra_context)

    def delete_link(self, obj):
        delete_url = reverse('admin:Contact_usermessage_delete', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="color: white; background-color: red; padding: 5px 10px; border-radius: 5px; text-decoration: none;">Delete</a>',
            delete_url
        )

    delete_link.short_description = 'Delete'

admin.site.register(UserMessage, UserMessageAdmin)


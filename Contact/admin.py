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
    list_display = (
        'serial_number_with_tag',
        'name',
        'email',
        'mobile',
        'created_at',
        'seen',
        'view_link',
        'delete_link'
    )
    search_fields = ('name', 'email', 'mobile')
    list_per_page = 20

    def get_queryset(self, request):
        """
        Attach the request object to the admin instance to calculate serial numbers.
        """
        self.request = request
        return super().get_queryset(request)

    def serial_number_with_tag(self, obj):
        """
        Display a serial number for each row, with a "New" tag if unseen.
        """
        queryset = self.get_queryset(self.request)
        start_index = int(self.request.GET.get('p', 0)) * self.list_per_page  # Pagination offset
        serial_number = list(queryset).index(obj) + 1 + start_index

        if not obj.seen:
            return format_html(
                '{} <span style="color: white; background-color: #385a7f; padding: 2px 5px; border-radius: 3px; font-size: 0.9em;">New</span>',
                serial_number
            )
        return serial_number

    serial_number_with_tag.short_description = "S.No"

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        Mark the message as seen when it's viewed in the admin.
        """
        obj = self.get_object(request, object_id)
        if obj and not obj.seen:
            obj.seen = True
            obj.save()
        return super().change_view(request, object_id, form_url, extra_context)

    def view_link(self, obj):
        """
        Provide a view link for the UserMessage.
        """
        view_url = reverse('admin:Contact_usermessage_change', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="color: white; background-color: #385a7f; padding: 5px 10px; border-radius: 5px; text-decoration: none;">View</a>',
            view_url
        )

    view_link.short_description = 'View'

    def delete_link(self, obj):
        """
        Provide a delete link for the UserMessage.
        """
        delete_url = reverse('admin:Contact_usermessage_delete', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="color: white; background-color: red; padding: 5px 10px; border-radius: 5px; text-decoration: none;">Delete</a>',
            delete_url
        )

    delete_link.short_description = 'Delete'


admin.site.register(UserMessage, UserMessageAdmin)




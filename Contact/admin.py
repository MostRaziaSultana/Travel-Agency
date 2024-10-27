from django.contrib import admin
from .models import *

# Register your models here.
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('address', 'mobile', 'hotline', 'email', 'support_mail')
    search_fields = ('address', 'email', 'mobile', 'hotline')

admin.site.register(ContactUs, ContactUsAdmin)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'created_at', 'seen')
    search_fields = ('name', 'email', 'mobile')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        if obj and not obj.seen:
            obj.seen = True
            obj.save()  # Mark as seen
        return super(UserMessageAdmin, self).change_view(request, object_id, form_url, extra_context)

admin.site.register(UserMessage, UserMessageAdmin)
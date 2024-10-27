from django.contrib import admin
from django.utils.html import format_html
from Deals.models import Package
from datetime import datetime


from .models import (AboutSection,
                     Destinationinfo,
                     Destination,
                     FooterContent,
                     FooterGallery,
                     FooterGalleryGroup,
                     GalleryImage,
                     Gallery,Header)

admin.site.register(Header)
admin.site.register(Destinationinfo)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('get_destination_name','package' ,'languages_spoken', 'visa_requirements', 'support_phone','show_on_homepage')

    def get_destination_name(self, obj):
        return obj.package.destination
    get_destination_name.short_description = 'Destination Name'

admin.site.register(Destination, DestinationAdmin)


class FooterGalleryInline(admin.TabularInline):
    model = FooterGallery
    fields = ['image']
    extra = 6

@admin.register(FooterGalleryGroup)
class FooterGalleryGroupAdmin(admin.ModelAdmin):
    inlines = [FooterGalleryInline]


class AboutSectionAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'image1',
        'image2',
        'list_item_1',
        'list_item_2',
        'list_item_3',
    )
    search_fields = ('title', 'description')
admin.site.register(AboutSection, AboutSectionAdmin)

class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 9

class GalleryAdmin(admin.ModelAdmin):
    inlines = [GalleryImageInline]

admin.site.register(Gallery, GalleryAdmin)


@admin.register(FooterContent)
class FooterContentAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'email', 'phone', 'copyright_year')
    search_fields = ('site_name', 'email', 'phone')
    readonly_fields = ('copyright_year',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('logo', 'site_name', 'info_text', 'address', 'phone', 'email')
        }),
        ('Social Media Links', {
            'fields': ('instagram', 'twitter', 'youtube', 'linkedin', 'facebook')
        }),
        ('Other Information', {
            'fields': ('copyright_year',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.copyright_year:
            obj.copyright_year = datetime.now().year
        super().save_model(request, obj, form, change)


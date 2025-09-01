from django.contrib import admin
from django.utils.html import format_html
from Deals.models import Package
from datetime import datetime
from django.utils.html import format_html
from django.urls import reverse


from .models import (AboutSection,
                     Destinationinfo,
                     FooterContent,
                     FooterGallery,
                     FooterGalleryGroup,
                     GalleryImage,
Banner,
                     Gallery,Header)

class HeaderAdmin(admin.ModelAdmin):
    list_display = ('title', 'logo_thumbnail', 'favicon_thumbnail', 'header_banner_thumbnail', 'update_link', 'delete_link')
    search_fields = ('title',)

    def logo_thumbnail(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="80" height="40" />', obj.logo.url)
        return "No Logo"
    logo_thumbnail.short_description = 'Logo'

    def favicon_thumbnail(self, obj):
        if obj.favicon:
            return format_html('<img src="{}" width="50" height="50" />', obj.favicon.url)
        return "No Favicon"
    favicon_thumbnail.short_description = 'Favicon'

    def header_banner_thumbnail(self, obj):
        if obj.header_banner:
            return format_html('<img src="{}" width="100" height="50" />', obj.header_banner.url)
        return "No Banner"
    header_banner_thumbnail.short_description = 'Header Banner'

    def update_link(self, obj):
        update_url = reverse('admin:Homepage_header_change', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="color: white; background-color: green; padding: 5px 10px; border-radius: 5px; text-decoration: none;">Update</a>',
            update_url
        )

    update_link.short_description = 'Update'

    def delete_link(self, obj):
        delete_url = reverse('admin:Homepage_header_delete', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="color: white; background-color: red; padding: 5px 10px; border-radius: 5px; text-decoration: none;">Delete</a>',
            delete_url
        )

    delete_link.short_description = 'Delete'

admin.site.register(Header, HeaderAdmin)
class DestinationinfoAdmin(admin.ModelAdmin):
    list_display = ('description', 'banner_image_thumbnail','update_link','delete_link', )
    search_fields = ('description',)

    def banner_image_thumbnail(self, obj):
        if obj.banner_image:
            return format_html('<img src="{}" width="100" height="100" />', obj.banner_image.url)
        return "No Image"
    banner_image_thumbnail.short_description = 'Banner Image'

    def update_link(self, obj):
        update_url = reverse('admin:Homepage_destinationinfo_change',
                             args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="color: white; background-color: green; padding: 5px 10px; border-radius: 5px; text-decoration: none;">Update</a>',
            update_url
        )

    update_link.short_description = 'Update'

    def delete_link(self, obj):
        delete_url = reverse('admin:Homepage_destinationinfo_delete',
                             args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="color: white; background-color: red; padding: 5px 10px; border-radius: 5px; text-decoration: none;">Delete</a>',
            delete_url
        )

    delete_link.short_description = 'Delete'


admin.site.register(Destinationinfo, DestinationinfoAdmin)


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
        # 'description',
        'image1',
        'image2',
        'list_item_1',
        'list_item_2',
        'list_item_3',
        'update_link',
        'delete_link',
    )
    search_fields = ('title', 'description')

    def update_link(self, obj):
        update_url = reverse('admin:Homepage_aboutsection_change',
                             args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="color: white; background-color: green; padding: 5px 10px; border-radius: 5px; text-decoration: none;">Update</a>',
            update_url
        )

    update_link.short_description = 'Update'

    def delete_link(self, obj):
        delete_url = reverse('admin:Homepage_aboutsection_delete',
                             args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="color: white; background-color: red; padding: 5px 10px; border-radius: 5px; text-decoration: none;">Delete</a>',
            delete_url
        )

    delete_link.short_description = 'Delete'

admin.site.register(AboutSection, AboutSectionAdmin)

class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 9

class GalleryAdmin(admin.ModelAdmin):
    inlines = [GalleryImageInline]

admin.site.register(Gallery, GalleryAdmin)


@admin.register(FooterContent)
class FooterContentAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'email', 'phone', 'update_link', 'delete_link')
    search_fields = ('site_name', 'email', 'phone')
    fieldsets = (
        ('Basic Information', {
            'fields': ('logo', 'site_name', 'info_text', 'address', 'phone', 'email')
        }),
        ('Social Media Links', {
            'fields': ('instagram', 'twitter', 'youtube', 'linkedin', 'facebook')
        }),
    )

    def update_link(self, obj):
        update_url = reverse('admin:Homepage_footercontent_change',
                             args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="color: white; background-color: green; padding: 5px 10px; border-radius: 5px; text-decoration: none;">Update</a>',
            update_url
        )

    update_link.short_description = 'Update'

    def delete_link(self, obj):
        delete_url = reverse('admin:Homepage_footercontent_delete',
                             args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="color: white; background-color: red; padding: 5px 10px; border-radius: 5px; text-decoration: none;">Delete</a>',
            delete_url
        )

    delete_link.short_description = 'Delete'

    def save_model(self, request, obj, form, change):
        if not obj.copyright_year:
            obj.copyright_year = datetime.now().year
        super().save_model(request, obj, form, change)



@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'login_banner_preview', 'registration_banner_preview', 'update_link', 'delete_link')

    def login_banner_preview(self, obj):
        if obj.login_banner:
            return format_html('<img src="{}" style="width: 100px; height: 60px;" />', obj.login_banner.url)
        return "No Image"

    def registration_banner_preview(self, obj):
        if obj.registration_banner:
            return format_html('<img src="{}" style="width: 100px; height: 60px;" />', obj.registration_banner.url)
        return "No Image"

    def update_link(self, obj):
        update_url = reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_change', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="color: white; background-color: green; padding: 5px 10px; border-radius: 5px; text-decoration: none;">Update</a>',
            update_url
        )

    def delete_link(self, obj):
        delete_url = reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_delete', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="color: white; background-color: red; padding: 5px 10px; border-radius: 5px; text-decoration: none;">Delete</a>',
            delete_url
        )

    update_link.short_description = "Update"
    delete_link.short_description = "Delete"
    login_banner_preview.short_description = "Login Banner Preview"
    registration_banner_preview.short_description = "Registration Banner Preview"

from django.contrib import admin
from django.utils.html import format_html


from .models import (AboutSection,
                     Destination,
                     DestinationImage,
                     FooterContent,
                     FooterGallery,
                     GalleryImage,
                     Gallery,Header)


admin.site.register(FooterContent)
admin.site.register(FooterGallery)
admin.site.register(Header)


class AboutSectionAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'image1',
        'image2',
        'list_item_1',
        'list_item_2',
        'list_item_3',
        'button_link'
    )
    search_fields = ('title', 'description')
admin.site.register(AboutSection, AboutSectionAdmin)


class DestinationImageInline(admin.TabularInline):
    model = DestinationImage
    extra = 6
    fields = ('image', 'name', 'show_on_homepage')
    readonly_fields = ('image',)

class DestinationAdmin(admin.ModelAdmin):
    inlines = [DestinationImageInline]

admin.site.register(Destination, DestinationAdmin)

class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 6

class GalleryAdmin(admin.ModelAdmin):
    inlines = [GalleryImageInline]

admin.site.register(Gallery, GalleryAdmin)


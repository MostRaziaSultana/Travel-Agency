from django.contrib import admin
from .models import Package, Booking,Tour_page,Destination,PaymentInfo,PaymentDescription
from django.db.models import Sum, Count, F, Avg
from datetime import datetime
from django.urls import reverse
from django.utils.html import format_html



@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('id','package_code', 'location', 'price', 'available_seats', 'start_date', 'end_date', 'status', 'creator', 'update_link', 'delete_link')
    search_fields = ('package_code', 'location', 'status')
    list_filter = ('status', 'start_date', 'end_date', 'hot_deal', 'show_on_homepage')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('package_code', 'location', 'price','child_price', 'duration', 'offer', 'creator', 'destination','short_description','overview','tour_plan_description' )
        }),
        ('Seats and Availability', {
            'fields': ('total_seats', 'available_seats', 'minimum_age')
        }),
        ('Date Information', {
            'fields': ('start_date', 'end_date')
        }),
        ('Images and Media', {
            'fields': ('image', 'bannerimage')
        }),
        ('Additional Information', {
            'fields': ('included', 'excluded', 'flight_details')
        }),
        ('Files', {
            'fields': ('travel_direction', 'documentations', 'logo_assets')
        }),
        ('Other', {
            'fields': ('status', 'hot_deal', 'show_on_homepage', 'departure_location')
        }),
    )
    list_per_page = 20

    def save_model(self, request, obj, form, change):
        if not obj.creator:
            obj.creator = request.user
        super().save_model(request, obj, form, change)

    def update_link(self, obj):
        update_url = reverse('admin:Deals_package_change', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="color: white; background-color: green; padding: 5px 10px; border-radius: 5px; text-decoration: none;">Update</a>',
            update_url
        )

    update_link.short_description = 'Update'

    def delete_link(self, obj):
        delete_url = reverse('admin:Deals_package_delete', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="color: white; background-color: red; padding: 5px 10px; border-radius: 5px; text-decoration: none;">Delete</a>',
            delete_url
        )

    delete_link.short_description = 'Delete'



class PaymentInfoAdmin(admin.ModelAdmin):
    list_display = (
        'id_with_tag',
        'payment_type',
        'payment_status',
        'transaction_id',
        'amount',
        'payment_date',
        'get_user',
        'seen',
        'update_link',
        'delete_link',
    )
    list_filter = ('payment_type', 'payment_date')
    search_fields = ('transaction_id', 'booking__creator__username', 'booking__creator__email')
    list_per_page = 20

    def id_with_tag(self, obj):
        """
        Display the ID with a "New" tag if the PaymentInfo is unseen.
        """
        if not obj.seen:
            return format_html(
                '{} <span style="color: white; background-color: #385a7f; padding: 2px 5px; border-radius: 3px; font-size: 0.9em;">New</span>',
                obj.id
            )
        return obj.id

    id_with_tag.short_description = "ID"

    def get_user(self, obj):
        """Display the user (creator) from the associated booking."""
        return obj.booking.creator

    get_user.short_description = 'User'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        if obj and not obj.seen:
            obj.seen = True
            obj.save()
        return super(PaymentInfoAdmin, self).change_view(request, object_id, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        if obj and not obj.seen:
            obj.seen = True
            obj.save()  # Mark as seen
        return super(PaymentInfoAdmin, self).change_view(request, object_id, form_url, extra_context)

    def update_link(self, obj):
        update_url = reverse('admin:Deals_paymentinfo_change', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="color: white; background-color: green; padding: 5px 10px; border-radius: 5px; text-decoration: none;">Update</a>',
            update_url
        )

    update_link.short_description = 'Update'

    def delete_link(self, obj):
        delete_url = reverse('admin:Deals_paymentinfo_delete', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="color: white; background-color: red; padding: 5px 10px; border-radius: 5px; text-decoration: none;">Delete</a>',
            delete_url
        )

    delete_link.short_description = 'Delete'


# Register the PaymentInfo model
admin.site.register(PaymentInfo, PaymentInfoAdmin)




class BookingAdmin(admin.ModelAdmin):
    list_display = ( 'id_with_tag', 'creator', 'package_id', 'booking_date', 'status', 'travel_status', 'price_at_booking','seen', 'update_link', 'delete_link')
    list_filter = ('status','travel_status', 'booking_date')
    search_fields = ('first_name', 'last_name', 'creator__username', 'package_id__destination')
    ordering = ('-booking_date',)  # Order by booking date descending
    list_per_page = 20

    def id_with_tag(self, obj):
        """
        Display the ID with a "New" tag if the Booking is unseen.
        """
        if not obj.seen:
            return format_html(
                '{} <span style="color: white; background-color: #385a7f; padding: 2px 5px; border-radius: 3px; font-size: 0.9em;">New</span>',
                obj.id
            )
        return obj.id

    id_with_tag.short_description = "ID"

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        if obj and not obj.seen:
            obj.seen = True
            obj.save()
        return super(BookingAdmin, self).change_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        if not obj.creator:
            obj.creator = request.user
        super().save_model(request, obj, form, change)

    def changelist_view(self, request, extra_context=None):
        # Fetch last 10 bookings
        last_bookings = Booking.objects.order_by('-created_at')[:10]
        print(f"Last 10 bookings fetched: {[booking.id for booking in last_bookings]}")

        # Pass the bookings to the context
        extra_context = extra_context or {}
        extra_context['last_bookings'] = last_bookings

        return super().changelist_view(request, extra_context=extra_context)


    def update_link(self, obj):
        update_url = reverse('admin:Deals_booking_change', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="color: white; background-color: green; padding: 5px 10px; border-radius: 5px; text-decoration: none;">Update</a>',
            update_url
        )

    update_link.short_description = 'Update'


    def delete_link(self, obj):
        delete_url = reverse('admin:Deals_booking_delete', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="color: white; background-color: red; padding: 5px 10px; border-radius: 5px; text-decoration: none;">Delete</a>',
            delete_url
        )

    delete_link.short_description = 'Delete'


admin.site.register(Booking, BookingAdmin)


@admin.register(Tour_page)
class TourPageAdmin(admin.ModelAdmin):
    list_display = ('discounted_destination_name', 'discount', 'banner_image_thumbnail', 'update_link', 'delete_link')
    search_fields = ('discounted_destination_name', 'discount')
    readonly_fields = ('banner_image_thumbnail',)
    list_per_page = 20

    def banner_image_thumbnail(self, obj):
        if obj.banner_image:
            return format_html('<img src="{}" width="100" height="50" />', obj.banner_image.url)
        return "No Image"

    banner_image_thumbnail.short_description = 'Banner Image'

    def update_link(self, obj):
        update_url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
        return format_html(
            '<a class="button" href="{}" style="color: white; background-color: green; padding: 5px 10px; border-radius: 5px; text-decoration: none;">Update</a>',
            update_url)

    update_link.short_description = 'Update'

    def delete_link(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
        return format_html(
            '<a class="button" href="{}" style="color: white; background-color: red; padding: 5px 10px; border-radius: 5px; text-decoration: none;">Delete</a>',
            delete_url)

    delete_link.short_description = 'Delete'

    fieldsets = (
        ('Basic Information', {
            'fields': ('discounted_destination_name', 'discount', 'banner_image')
        }),
    )


class DestinationAdmin(admin.ModelAdmin):
    list_display = ('id','get_destination_name','package' ,'languages_spoken', 'visa_requirements', 'support_phone','show_on_homepage', 'update_link', 'delete_link')
    list_per_page = 20

    def get_destination_name(self, obj):
        return obj.package.destination
    get_destination_name.short_description = 'Destination Name'

    def update_link(self, obj):
        update_url = reverse('admin:Deals_destination_change', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="color: white; background-color: green; padding: 5px 10px; border-radius: 5px; text-decoration: none;">Update</a>',
            update_url
        )

    update_link.short_description = 'Update'

    def delete_link(self, obj):
        delete_url = reverse('admin:Deals_destination_delete', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="color: white; background-color: red; padding: 5px 10px; border-radius: 5px; text-decoration: none;">Delete</a>',
            delete_url
        )

    delete_link.short_description = 'Delete'


admin.site.register(Destination, DestinationAdmin)


@admin.register(PaymentDescription)
class PaymentDetailsAdmin(admin.ModelAdmin):
    list_display = ('id',)
    search_fields = ('payment_description',)



from django.contrib import admin
from .models import Package, Booking,Tour_page,Destination,PaymentInfo,PaymentDescription
from django.db.models import Sum, Count, F, Avg
from datetime import datetime
from django.urls import reverse
from django.utils.html import format_html



@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('serial_number','package_code', 'location', 'price', 'available_seats', 'start_date', 'end_date', 'status', 'creator', 'update_link', 'delete_link')
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

    def serial_number(self, obj):
        """Return the serial number for the row."""
        # Use the current queryset for the model admin and get the row's index
        # Note: `self.model` is the model for the current admin
        return list(self.get_queryset(obj).values_list('id', flat=True)).index(obj.id) + 1

    serial_number.short_description = 'S.No'  # Display name for the column
    serial_number.admin_order_field = 'id'  # Allow sorting by the model's primary key



class PaymentInfoAdmin(admin.ModelAdmin):
    list_display = (
        'serial_number_with_tag',
        'payment_type',
        'payment_status',
        'transaction_id',
        'amount',
        'payment_date',
        'get_user',
        'update_link',
        'delete_link',
    )
    list_filter = ('payment_type', 'payment_date')
    search_fields = ('transaction_id', 'booking__creator__username', 'booking__creator__email')
    list_per_page = 20

    def serial_number_with_tag(self, obj):
        """
        Display the serial number with a "New" tag if the PaymentInfo is unseen.
        """
        request = self.request
        queryset = self.get_queryset(request)
        serial_number = list(queryset).index(obj) + 1

        tag_html = ""
        if not obj.seen:
            tag_html = (
                '<br><span style="color: white; background-color: #385a7f; '
                'padding: 2px 5px; border-radius: 3px; font-size: 0.9em;">New</span>'
            )
        return format_html(f'{serial_number}{tag_html}')

    serial_number_with_tag.short_description = "S.No"

    def get_queryset(self, request):
        """
        Attach the request to the admin instance and fetch the queryset.
        """
        self.request = request
        return super().get_queryset(request)

    def get_user(self, obj):
        """Display the user (creator) from the associated booking."""
        return obj.booking.creator

    get_user.short_description = 'User'

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
    list_display = ('serial_number_with_tag', 'creator', 'package_id', 'booking_date', 'status',
                    'travel_status', 'price_at_booking', 'seen', 'update_link', 'delete_link')
    list_filter = ('status', 'travel_status', 'booking_date')
    search_fields = ('first_name', 'last_name', 'creator__username', 'package_id__destination')
    ordering = ('-booking_date',)  # Order by booking date descending
    list_per_page = 20

    def serial_number_with_tag(self, obj):
        """
        Display the serial number with the "New" tag below it if the booking is unseen.
        """
        # Find the position of the current object in the queryset
        request = self.request
        queryset = self.get_queryset(request)
        serial_number = list(queryset).index(obj) + 1

        tag_html = ""
        if not obj.seen:
            tag_html = (
                '<br><span style="color: white; background-color: #385a7f; '
                'padding: 2px 5px; border-radius: 3px; font-size: 0.9em;">New</span>'
            )
        return format_html(f'{serial_number}{tag_html}')

    serial_number_with_tag.short_description = "S.No"

    def get_queryset(self, request):
        """
        Attach the request to the admin instance and fetch the queryset.
        """
        self.request = request
        return super().get_queryset(request)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        if obj and not obj.seen:
            obj.seen = True
            obj.save()
        return super().change_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        if not obj.creator:
            obj.creator = request.user
        super().save_model(request, obj, form, change)

    def update_link(self, obj):
        update_url = reverse('admin:Deals_booking_change', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="color: white; background-color: green; '
            'padding: 5px 10px; border-radius: 5px; text-decoration: none;">Update</a>',
            update_url
        )

    update_link.short_description = 'Update'

    def delete_link(self, obj):
        delete_url = reverse('admin:Deals_booking_delete', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="color: white; background-color: red; '
            'padding: 5px 10px; border-radius: 5px; text-decoration: none;">Delete</a>',
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
    list_display = (
        'serial_number',
        'get_destination_name',
        'package',
        'languages_spoken',
        'visa_requirements',
        'support_phone',
        'show_on_homepage',
        'update_link',
        'delete_link',
    )
    list_per_page = 20

    def serial_number(self, obj):
        """
        Display a serial number for each row in the admin list.
        """
        # Calculate the index of the object in the current page of the queryset
        request = self.request
        queryset = self.get_queryset(request)
        start_index = request.GET.get('p', 0)  # Page number
        index = list(queryset).index(obj) + 1 + int(start_index) * self.list_per_page
        return index

    serial_number.short_description = "S.No"

    def get_queryset(self, request):
        """
        Attach the request object to the admin instance to calculate serial numbers.
        """
        self.request = request
        return super().get_queryset(request)

    def get_destination_name(self, obj):
        """
        Return the destination name from the associated package.
        """
        return obj.package.destination

    get_destination_name.short_description = 'Destination Name'

    def update_link(self, obj):
        """
        Provide an update link for the destination.
        """
        update_url = reverse('admin:Deals_destination_change', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="color: white; background-color: green; padding: 5px 10px; border-radius: 5px; text-decoration: none;">Update</a>',
            update_url
        )

    update_link.short_description = 'Update'

    def delete_link(self, obj):
        """
        Provide a delete link for the destination.
        """
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



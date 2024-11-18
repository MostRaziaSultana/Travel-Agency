from django.contrib import admin
from .models import Package, Booking,Tour_page,Destination,PaymentInfo
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

class PaymentInfoInline(admin.TabularInline):
    model = PaymentInfo
    extra = 0  # No additional empty rows
    readonly_fields = ['payment_type', 'account_no', 'transaction_id', 'amount', 'payment_date']
    can_delete = False  # Disable delete option
    verbose_name = "Payment Info"
    verbose_name_plural = "Payment Info"

    def has_add_permission(self, request, obj=None):
        """
        Prevent adding new PaymentInfo rows in the inline.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Prevent deleting PaymentInfo rows in the inline.
        """
        return False

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'package_id', 'booking_date', 'status', 'payment_status', 'travel_status', 'price_at_booking', 'update_link', 'delete_link')
    list_filter = ('status', 'payment_status', 'travel_status', 'booking_date')
    search_fields = ('first_name', 'last_name', 'creator__username', 'package_id__destination')
    ordering = ('-booking_date',)  # Order by booking date descending
    inlines = [PaymentInfoInline]
    list_per_page = 20

    def display_payment_info(self, obj):
        """
        Display a summary of payment info for the booking.
        """
        payments = obj.payments.all()  # Access related PaymentInfo objects via related_name
        if not payments:
            return "No payments"
        return ', '.join([f"{payment.payment_type} ({payment.amount})" for payment in payments])

    display_payment_info.short_description = 'Payment Info'

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



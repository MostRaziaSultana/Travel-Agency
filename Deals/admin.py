from django.contrib import admin
from .models import Package, Booking,Tour_page,Destination
from django.db.models import Sum, Count, F, Avg
from datetime import datetime


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('id','package_code', 'location', 'price', 'available_seats', 'start_date', 'end_date', 'status', 'creator')
    search_fields = ('package_code', 'location', 'status')
    list_filter = ('status', 'start_date', 'end_date', 'hot_deal', 'show_on_homepage')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('package_code', 'location', 'price','child_price', 'duration', 'offer', 'creator', 'destination','short_description','overview')
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

    # def has_view_permission(self, request, obj=None):
    #     return request.user.has_perm('Deals.can_crud_package')
    #
    # def has_change_permission(self, request, obj=None):
    #     return request.user.has_perm('Deals.can_crud_package')
    #
    # def has_delete_permission(self, request, obj=None):
    #     return request.user.has_perm('Deals.can_crud_package')
    #
    # def has_add_permission(self, request):
    #     return request.user.has_perm('Deals.can_crud_package')
    #
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(creator=request.user)
    # def changelist_view(self, request, extra_context=None):

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'package_id', 'booking_date', 'status', 'payment_status', 'travel_status', 'price_at_booking')
    list_filter = ('status', 'payment_status', 'travel_status', 'booking_date')
    search_fields = ('first_name', 'last_name', 'creator__username', 'package_id__destination')
    ordering = ('-booking_date',)  # Order by booking date descending
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


admin.site.register(Booking, BookingAdmin)
admin.site.register(Tour_page)


class DestinationAdmin(admin.ModelAdmin):
    list_display = ('id','get_destination_name','package' ,'languages_spoken', 'visa_requirements', 'support_phone','show_on_homepage')

    def get_destination_name(self, obj):
        return obj.package.destination
    get_destination_name.short_description = 'Destination Name'

admin.site.register(Destination, DestinationAdmin)



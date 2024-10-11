from django.contrib import admin
from .models import Package, Booking

class PackageAdmin(admin.ModelAdmin):
    list_display = ('package_code', 'package_name', 'destination', 'price', 'available_seats', 'status', 'creator', 'created_at', 'updated_at')
    search_fields = ('package_code', 'package_name', 'destination')
    list_filter = ('status', 'creator', 'start_date', 'end_date')

    def has_view_permission(self, request, obj=None):
        return request.user.has_perm('Home.can_crud_package')

    def has_change_permission(self, request, obj=None):
        return request.user.has_perm('Home.can_crud_package')

    def has_delete_permission(self, request, obj=None):
        return request.user.has_perm('Home.can_crud_package')

    def has_add_permission(self, request):
        return request.user.has_perm('Home.can_crud_package')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Allow superusers to see all packages
        return qs.filter(creator=request.user)


class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'package_id', 'booking_date', 'status', 'payment_status', 'travel_status', 'price_at_booking', 'created_at', 'updated_at')
    search_fields = ('customer_id__username', 'package_id__package_name')
    list_filter = ('status', 'payment_status', 'travel_status', 'booking_date')


admin.site.register(Package, PackageAdmin)
admin.site.register(Booking, BookingAdmin)

from django.contrib import admin
from .models import Package, Booking,Tour_page
from django.db.models import Sum, Count, F, Avg
from django.template.response import TemplateResponse
from datetime import datetime

from django.contrib import admin
from django.urls import path

def shoily_register(model, admin_manager=None):
    admin_site.register(model, admin_manager)
    admin.site.register(model, admin_manager)

# Create a custom AdminSite
class CustomAdminSite(admin.AdminSite):
    def index(self, request, extra_context=None):
        # Fetch the permitted app list
        app_list = self.get_app_list(request)

        # Add your custom context
        context = {
            'custom_var': 'This is a custom context for the admin index page.',
            'other_data': 'You can add any data here that you need in your template.',
            'app_list': app_list,  # Include the permitted app list
        }

        # Include any additional context passed in
        if extra_context is not None:
            context.update(extra_context)

        # Call the parent class's index method with the updated context
        return super().index(request, extra_context=context)

# Use the default admin site (no need to register models)
admin_site = CustomAdminSite(name='custom_admin')


class PackageAdmin(admin.ModelAdmin):
    # change_form_template = 'admin/package_change_form.html'
    change_list_template = 'admin/package_analytics.html'
    # list_display = ('package_code', 'package_name', 'destination', 'price', 'available_seats', 'status', 'creator', 'created_at', 'updated_at')
    search_fields = ('package_code', 'package_name', 'destination')
    # list_filter = ('status', 'creator', 'start_date', 'end_date')

    def has_view_permission(self, request, obj=None):
        return request.user.has_perm('Deals.can_crud_package')

    def has_change_permission(self, request, obj=None):
        return request.user.has_perm('Deals.can_crud_package')

    def has_delete_permission(self, request, obj=None):
        return request.user.has_perm('Deals.can_crud_package')

    def has_add_permission(self, request):
        return request.user.has_perm('Deals.can_crud_package')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(creator=request.user)
    def changelist_view(self, request, extra_context=None):
        # Analytics Queries

        # 1. Total Revenue per Package
        revenue_data = Booking.objects.values('package_id__location').annotate(
            total_revenue=Sum('price_at_booking')
        )

        # 2. Booking Status Breakdown
        status_data = Booking.objects.values('status').annotate(
            count=Count('status')
        )

        # 3. Payment Status Distribution
        payment_status_data = Booking.objects.values('payment_status').annotate(
            count=Count('payment_status')
        )

        # 4. Popular Destination Breakdown
        destination_data = Package.objects.values('destination').annotate(
            booking_count=Count('booking__id')
        )

        # 5. Package Availability Over Time
        availability_data = Package.objects.values('available_seats', 'updated_at')

        # 6. Booking Trend Over Time
        booking_trend_data = Booking.objects.values('booking_date').annotate(
            count=Count('package_id')
        )

        # 7. Customer Booking Frequency
        customer_frequency_data = Booking.objects.values('customer_id').annotate(
            booking_count=Count('customer_id')
        )

        # 8. Top Booked Packages
        top_packages_data = Booking.objects.values('package_id__location').annotate(
            booking_count=Count('package_id')
        ).order_by('-booking_count')

        # 9. Travel Status Tracking
        travel_status_data = Booking.objects.values('travel_status').annotate(
            count=Count('travel_status')
        )

        # 10. Package Cancellation Rate
        cancellation_rate_data = Package.objects.values('status', 'package_code')

        # 11. Average Price per Destination
        avg_price_data = Package.objects.values('destination').annotate(
            avg_price=Avg('price')
        )

        # 12. Booking Payment Status per Month
        payment_status_per_month_data = Booking.objects.values('payment_status', 'booking_date__month').annotate(
            count=Count('id')
        )

        # 13. Packages with Additional Services
        additional_services_data = Package.objects.values('additional_services').annotate(
            count=Count('additional_services')
        )

        # 14. Customer Retention Rate
        total_customers = Booking.objects.values('customer_id').distinct().count()
        repeat_customers = Booking.objects.values('customer_id').annotate(
            booking_count=Count('customer_id')
        ).filter(booking_count__gt=1).count()
        customer_retention_rate = (repeat_customers / total_customers) * 100 if total_customers > 0 else 0

        # 15. Package Booking Completion Time
        booking_completion_time_data = Booking.objects.annotate(
            completion_time=F('updated_at') - F('created_at')
        ).values('completion_time')

        # 16. Upcoming Packages
        upcoming_packages_data = Package.objects.filter(
            start_date__gte=datetime.now()
        ).values('location', 'start_date', 'available_seats')

        # 17. Total Seats vs. Booked Seats per Package
        seat_data = Package.objects.annotate(
            booked_seats=F('total_seats') - F('available_seats')
        ).values('location', 'total_seats', 'booked_seats')

        # 18. Average Booking Price
        avg_booking_price = Booking.objects.aggregate(Avg('price_at_booking'))['price_at_booking__avg']

        # 19. Booking vs. Cancellation Rate
        booking_vs_cancellation_data = Booking.objects.values('status', 'booking_date').annotate(
            count=Count('id')
        )

        # 20. Total Bookings
        total_bookings = Booking.objects.count()

        # 21. Existing packages
        packages = Package.objects.all()


        # Passing the context
        extra_context = extra_context or {
            'revenue_data': revenue_data,
            'status_data': status_data,
            'payment_status_data': payment_status_data,
            'destination_data': destination_data,
            'availability_data': availability_data,
            'booking_trend_data': booking_trend_data,
            'customer_frequency_data': customer_frequency_data,
            'top_packages_data': top_packages_data,
            'travel_status_data': travel_status_data,
            'cancellation_rate_data': cancellation_rate_data,
            'avg_price_data': avg_price_data,
            'payment_status_per_month_data': payment_status_per_month_data,
            'additional_services_data': additional_services_data,
            'customer_retention_rate': customer_retention_rate,
            'booking_completion_time_data': booking_completion_time_data,
            'upcoming_packages_data': upcoming_packages_data,
            'seat_data': seat_data,
            'avg_booking_price': avg_booking_price,
            'booking_vs_cancellation_data': booking_vs_cancellation_data,
            'total_bookings': total_bookings,
            'packages': packages,
        }

        return super().changelist_view(request, extra_context=extra_context)


class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'package_id', 'booking_date', 'status', 'payment_status', 'travel_status', 'price_at_booking', 'created_at', 'updated_at')
    search_fields = ('customer_id__username', 'package_id__package_name')
    list_filter = ('status', 'payment_status', 'travel_status', 'booking_date')


shoily_register(Package, PackageAdmin)
shoily_register(Booking, BookingAdmin)
shoily_register(Tour_page)



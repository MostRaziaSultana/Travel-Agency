from .models import FooterContent,FooterGallery,Header
from Contact.models import ContactUs,UserMessage
from Deals.models import Booking, Package,Destination,Tour_page
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.utils.timezone import now
def footer_content(request):
    return {
        'footer_content': FooterContent.objects.first(),
    }

def footer_gallery(request):
    return {
        'footer_gallery': FooterGallery.objects.all()
    }

def header(request):
    return {
        'header': Header.objects.first()
    }

def contact_us(request):
    return {
        'contact_us': ContactUs.objects.first()
    }

def last_bookings(request):
    bookings = Booking.objects.order_by('-created_at')[:10]

    total_packages = Package.objects.count()
    total_booked = Booking.objects.filter(status='Booked').count()
    total_messages = UserMessage.objects.count()
    total_destinations = Destination.objects.count()
    total_users = User.objects.count()
    total_unseen_messages = UserMessage.objects.filter(seen=False).count()


    return {
        'last_bookings': bookings,
        'total_packages': total_packages,
        'total_booked': total_booked,
        'total_messages': total_messages,
        'total_destinations': total_destinations,
        'total_users': total_users,
        'total_unseen_messages': total_unseen_messages,
    }


def get_visualization_data():
    # 1. Number of Bookings by Package
    bookings_by_package = (
        Booking.objects.values('package_id__destination')  # Aggregate by destination name
        .annotate(count=Count('id'))
        .order_by('package_id__destination')
    )
    bookings_by_package_list = [(entry['package_id__destination'], entry['count']) for entry in bookings_by_package]

    # 2. Booking Status Counts
    booking_status_counts = (
        Booking.objects.values('status')
        .annotate(count=Count('id'))
        .order_by('status')
    )
    booking_status_counts_list = [(entry['status'], entry['count']) for entry in booking_status_counts]

    # 3. Travel Status by Package
    travel_status_by_package = (
        Booking.objects.values('package_id__destination', 'travel_status')
        .annotate(count=Count('id'))
        .order_by('package_id__destination', 'travel_status')
    )
    travel_status_by_package_list = [
        (entry['package_id__destination'], entry['travel_status'], entry['count'])
        for entry in travel_status_by_package
    ]

    # 4. Revenue by Package
    revenue_by_package = (
        Booking.objects.values('package_id__destination')
        .annotate(total_revenue=Sum('price_at_booking'))
        .order_by('package_id__destination')
    )
    revenue_by_package_list = [
        (entry['package_id__destination'], entry['total_revenue']) for entry in revenue_by_package
    ]

    # 5. Discounted Destinations (Tour_page)
    discounted_destinations = (
        Tour_page.objects.values('discounted_destination_name', 'discount')
        .order_by('discounted_destination_name')
    )
    discounted_destinations_list = [
        (entry['discounted_destination_name'], entry['discount']) for entry in discounted_destinations
    ]

    return {
        "bookings_by_package": bookings_by_package_list,
        "booking_status_counts": booking_status_counts_list,
        "travel_status_by_package": travel_status_by_package_list,
        "revenue_by_package": revenue_by_package_list,
        "discounted_destinations": discounted_destinations_list,
    }
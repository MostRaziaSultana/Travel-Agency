from .models import FooterContent,FooterGallery,Header,Banner
from Contact.models import ContactUs,UserMessage
from Deals.models import Booking, Package,Destination,Tour_page,PaymentInfo
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

def banner(request):
    return {
        'banner': Banner.objects.first()
    }


def last_bookings(request):
    bookings = Booking.objects.order_by('-created_at')[:10]

    total_packages = Package.objects.count()
    total_booked = Booking.objects.filter(status='Booked').count()
    total_messages = UserMessage.objects.count()
    total_destinations = Destination.objects.count()
    total_users = User.objects.count()
    total_unseen_messages = UserMessage.objects.filter(seen=False).count()
    total_paid_count = PaymentInfo.objects.filter(payment_status='Paid').count()
    total_payments = PaymentInfo.objects.count()
    total_refunded_count = PaymentInfo.objects.filter(payment_status='Refunded').count()

    total_unseen_payments = PaymentInfo.objects.filter(seen=False).count()
    total_unseen_bookings = Booking.objects.filter(seen=False).count()


    return {
        'last_bookings': bookings,
        'total_packages': total_packages,
        'total_booked': total_booked,
        'total_messages': total_messages,
        'total_destinations': total_destinations,
        'total_users': total_users,
        'total_unseen_messages': total_unseen_messages,
        'total_paid_count': total_paid_count,
        'total_payments':total_payments,
        'total_refunded_count':total_refunded_count,
        'total_unseen_payments':total_unseen_payments,
        'total_unseen_bookings':total_unseen_bookings,
    }


def get_visualization_data(request):
    # 1. Number of Bookings by Package
    bookings_by_package = (
        Booking.objects.values('package_id__destination')  # Aggregate by destination name
        .annotate(count=Count('id'))
        .order_by('package_id__destination')
    )
    bookings_by_package_list = [[entry['package_id__destination'], entry['count']] for entry in bookings_by_package]
    return{"bookings_by_package": bookings_by_package_list}
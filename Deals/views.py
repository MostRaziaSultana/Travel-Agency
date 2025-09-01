from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q
import datetime
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def tours(request):
    tours = Package.objects.all()
    tour_extra = Tour_page.objects.first()

    service = request.GET.get('service')
    date = request.GET.get('date')

    if service:
        tours = tours.filter(
            Q(destination__icontains=service) | Q(location__icontains=service)
        )
    if date:
            Q(start_date__icontains=date) | Q(end_date__icontains=date)


    search_query = request.GET.get('search-field')

    if search_query:
        tours = tours.filter(
            Q(destination__icontains=search_query) | Q(location__icontains=search_query)
        )

    paginator = Paginator(tours, 3)
    page_number = request.GET.get('page', 1)
    tours = paginator.get_page(page_number)


    return render(request, 'Tour/tours.html', { 'tours': tours,
                                                'results_start': tours.start_index(),
                                                'results_end': tours.end_index(),
                                                'total_results': tours.paginator.count,
                                                'page_obj': tours,
                                                # 'search_query': search_query,
                                                'tour_extra':tour_extra,
                                                'service': service,
                                                'date': date,
                                                })


def tour_details(request, id):
    tour_details = Package.objects.get(id=id)
    tour_extra = Tour_page.objects.first()
    return render(request, 'Tour/tour_details.html', { 'tour_details': tour_details,
                                                       'tour_extra':tour_extra})


# @csrf_exempt
# def bookings(request, id):
#     tour_details = get_object_or_404(Package, id=id)
#
#     if request.method == "POST":
#         # Determine which form is being submitted
#         if 'full_name' in request.POST:  # Booking form submitted
#             full_name = request.POST.get('full_name')
#             phone = request.POST.get('phone')
#             address = request.POST.get('address')
#             email = request.POST.get('email')
#             adult = int(request.POST.get('adults', 1))
#             children = int(request.POST.get('children', 0))
#             message = request.POST.get('message')
#
#             total_guests = adult + children
#
#             if tour_details.available_seats >= total_guests:
#                 total_price = (adult * tour_details.price) + (children * tour_details.child_price)
#
#                 booking = Booking.objects.create(
#                     creator=request.user,
#                     package_id=tour_details,
#                     booking_date=datetime.date.today(),
#                     status="Booked",
#                     travel_status="Scheduled",
#                     price_at_booking=total_price,
#                     full_name=full_name,
#                     phone=phone,
#                     address=address,
#                     email=email,
#                     adult=adult,
#                     children=children,
#                     message=message,
#                 )
#
#                 tour_details.available_seats -= total_guests
#                 tour_details.save()
#
#                 messages.success(request, "Booking successful! Proceed to payment.")
#                 return redirect('payment', booking_id=booking.id)  # Redirect to payment page
#
#             else:
#                 messages.warning(request, "Not enough available seats.")
#                 return redirect(request.META.get('HTTP_REFERER', '/'))
#
#
#     return render(request, 'Booking/booking.html', {'tour_details': tour_details})

@csrf_exempt
def bookings(request, id):
    tour_details = get_object_or_404(Package, id=id)

    if request.method == "POST":
        # Retrieve form data
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        email = request.POST.get('email')
        adult = int(request.POST.get('adults', 1))
        children = int(request.POST.get('children', 0))
        message = request.POST.get('message')

        total_guests = adult + children

        if tour_details.available_seats >= total_guests:
            total_price = (adult * tour_details.price) + (children * tour_details.child_price)

            if request.user.is_authenticated:
                booking = Booking.objects.create(
                    creator=request.user,
                    package_id=tour_details,
                    booking_date=datetime.date.today(),
                    status="Booked",
                    travel_status="Scheduled",
                    price_at_booking=total_price,
                    full_name=full_name,
                    phone=phone,
                    address=address,
                    email=email,
                    adult=adult,
                    children=children,
                    message=message,
                )

                tour_details.available_seats -= total_guests
                tour_details.save()

                messages.success(request, "Booking successful! Proceed to payment.")
                return redirect('payment', booking_id=booking.id)

            else:
                session_booking = {
                    'package_id': tour_details.id,
                    'full_name': full_name,
                    'phone': phone,
                    'address': address,
                    'email': email,
                    'adult': adult,
                    'children': children,
                    'message': message,
                    'total_price': float(total_price),
                    'booking_date': str(datetime.date.today()),
                }
                request.session['booking'] = session_booking

                messages.success(request, "Booking successful! Proceed to payment.")
                return redirect('payment_session')

        else:
            messages.warning(request, "Not enough available seats.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, 'Booking/booking.html', {'tour_details': tour_details})


@csrf_exempt
def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    tour_details = booking.package_id
    payment_description = PaymentDescription.objects.first()

    if request.method == "POST":
        payment_type = request.POST.get('payment_type')
        account_no = request.POST.get('account_no')
        transaction_id = request.POST.get('transaction')
        amount = request.POST.get('amount')
        payment_date = request.POST.get('payment_date')

        PaymentInfo.objects.create(
            booking=booking,
            payment_type=payment_type,
            account_no=account_no,
            transaction_id=transaction_id,
            amount=amount,
            payment_date=payment_date if payment_date else None
        )

        booking.payment_status = "Pending"
        booking.save()

        messages.success(request, "Payment successful!")
        return redirect('success', booking_id=booking.id)

    return render(request, 'Booking/payment.html', {
        'booking': booking,
        'tour_details': tour_details,
        'payment_description':payment_description,
    })



def success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    tour_details = booking.package_id
    return render(request, 'Booking/success.html', {
        'booking': booking,
        'tour_details': tour_details,
    })


@csrf_exempt
def payment_session(request):
    session_booking = request.session.get('booking')

    if not session_booking:
        messages.error(request, "No booking information found in session.")
        return redirect('tours')

    package = get_object_or_404(Package, id=session_booking['package_id'])
    payment_description = PaymentDescription.objects.first()

    if request.method == "POST":
        payment_type = request.POST.get('payment_type')
        account_no = request.POST.get('account_no')
        transaction_id = request.POST.get('transaction')
        amount = request.POST.get('amount')
        payment_date = request.POST.get('payment_date')

        # Check if booking exists in session, if not, create one for the anonymous user
        if 'booking_id' not in session_booking:
            booking = Booking.objects.create(
                creator=None,  # No authenticated user, so set it to None
                package_id=package,
                booking_date=datetime.date.today(),
                status="Booked",
                travel_status="Scheduled",
                price_at_booking=session_booking['total_price'],
                full_name=session_booking['full_name'],
                phone=session_booking['phone'],
                address=session_booking['address'],
                email=session_booking['email'],
                adult=session_booking['adult'],
                children=session_booking['children'],
                message=session_booking['message'],
            )
            session_booking['booking_id'] = booking.id
            request.session['booking'] = session_booking  # Update session with new booking_id
        else:
            booking = Booking.objects.get(id=session_booking['booking_id'])

        # Create the payment record with the associated booking
        PaymentInfo.objects.create(
            booking=booking,  # Use the booking created or fetched
            payment_type=payment_type,
            account_no=account_no,
            transaction_id=transaction_id,
            amount=amount,
            payment_date=payment_date if payment_date else None
        )

        messages.success(request, "Payment successful!")
        return redirect('success_session')

    return render(request, 'Booking/payment.html', {
        'session_booking': session_booking,
        'tour_details': package,
        'payment_description': payment_description,
    })



def success_session(request):
    session_booking = request.session.get('booking')
    if not session_booking:
        messages.error(request, "No booking information found in session.")
        return redirect('tours')

    package = get_object_or_404(Package, id=session_booking['package_id'])

    return render(request, 'Booking/success.html', {
        'session_booking': session_booking,
        'tour_details': package,
    })

from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q
import datetime
from django.contrib import messages

# Create your views here.


def tours(request):
    tours = Package.objects.all()
    tour_extra = Tour_page.objects.first()

    service = request.GET.get('service')
    travel_type = request.GET.get('travel_type')
    date = request.GET.get('date')


    # if service:
    #     tours = tours.filter(Q(destination__icontains=service))
    # if date:
    #     tours = tours.filter(Q(tour_date__icontains=date))


    search_query = request.GET.get('search-field')
    if search_query:
        tours = Package.objects.filter(Q(destination__icontains=search_query))

    paginator = Paginator(tours, 2)
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
                                                'travel_type': travel_type,
                                                'date': date,
                                                })


def tour_details(request, id):
    tour_details = Package.objects.get(id=id)
    tour_extra = Tour_page.objects.first()
    return render(request, 'Tour/tour_details.html', { 'tour_details': tour_details,
                                                       'tour_extra':tour_extra})


def bookings(request, id):
    tour_details = get_object_or_404(Package, id=id)

    if request.method == "POST":
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        address_1 = request.POST.get('address1')
        address_2 = request.POST.get('address2')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip')
        adult = int(request.POST.get('adults', 1))
        children = int(request.POST.get('children', 0))
        message = request.POST.get('message')

        # Calculate total number of guests
        total_guests = adult + children


        if tour_details.available_seats >= total_guests:

            total_price = (adult * tour_details.price) + (children * tour_details.child_price)


            booking = Booking.objects.create(
                customer_id=request.user,
                package_id=tour_details,
                booking_date=datetime.date.today(),
                status="Pending",
                payment_status="Pending",
                travel_status="Scheduled",
                price_at_booking=total_price,
                first_name=first_name,
                last_name=last_name,
                address_1=address_1,
                address_2=address_2,
                city=city,
                zip_code=zip_code,
                adult=adult,
                children=children,
                message=message,
            )

            tour_details.available_seats -= total_guests
            tour_details.save()

        else:

            messages.warning(request, "Not enough available seats.")
            return redirect(request.META['HTTP_REFERER'])

    return render(request, 'Booking/booking.html', {'tour_details': tour_details})

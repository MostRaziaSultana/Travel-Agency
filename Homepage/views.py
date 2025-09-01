from django.shortcuts import render
from .models import *
from Deals.models import Package,Tour_page,Destination
from django.core.paginator import Paginator

# Create your views here.
def home(request):

    about_section = AboutSection.objects.first()
    destinations = Destination.objects.all()
    destination_info = Destinationinfo.objects.first()
    header = Header.objects.first()
    tours = Package.objects.all()

    return render(request, 'home.html', {
        'about_section': about_section,
        'destinations': destinations,
        'destination_info':destination_info,
        'tours':tours,
        'header':header
    })


def gallery(request):
    banner_image = Gallery.objects.first()
    if banner_image:
        all_images = banner_image.images.all()
    else:
        all_images = []
    paginator = Paginator(all_images, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'gallery.html', {
        'banner_image': banner_image,
        'page_obj': page_obj
    })


# def destinations(request):
#     destinations = Destination.objects.all()
#     destination_info = Destinationinfo.objects.first()
#     return render(request, 'Tour/destinations.html', { 'destinations': destinations,
#         'destination_info':destination_info,})


def destinations(request):
    destinations_list = Destination.objects.all()
    destination_info = Destinationinfo.objects.first()

    paginator = Paginator(destinations_list, 3)
    page_number = request.GET.get('page', 1)
    destinations = paginator.get_page(page_number)

    return render(request, 'Tour/destinations.html', {
        'destinations': destinations,
        'results_start': destinations.start_index(),
        'results_end': destinations.end_index(),
        'total_results': destinations.paginator.count,
        'page_obj': destinations,
        'destination_info': destination_info,
    })


def destination_details(request, id):
    destination_details = Destination.objects.get(id=id)
    tour_extra = Tour_page.objects.first()

    return render(request, 'Tour/destination_details.html', {'destination_details':destination_details,
                                                             'tour_extra':tour_extra})




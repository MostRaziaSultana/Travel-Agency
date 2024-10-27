from django.shortcuts import render
from .models import *
from Deals.models import Package,Tour_page
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
    images = Gallery.objects.first()
    return render(request, 'gallery.html', {'banner_image': banner_image, 'gallery': images})


def destinations(request):
    destinations = Destination.objects.all()
    destination_info = Destinationinfo.objects.first()
    return render(request, 'Tour/destinations.html', { 'destinations': destinations,
        'destination_info':destination_info,})


def destination_details(request, id):
    destination_details = Destination.objects.get(id=id)
    tour_extra = Tour_page.objects.first()

    return render(request, 'Tour/destination_details.html', {'destination_details':destination_details,
                                                             'tour_extra':tour_extra})


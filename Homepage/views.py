from django.shortcuts import render
from .models import *
from Deals.models import Package
# Create your views here.
def home(request):

    about_section = AboutSection.objects.first()
    destinations = DestinationImage.objects.all()
    destination_info = Destination.objects.first()
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
    destinations = DestinationImage.objects.all()
    destination_info = Destination.objects.first()
    return render(request, 'Tour/destinations.html', { 'destinations': destinations,
        'destination_info':destination_info,})


from .models import FooterContent,FooterGallery,Header
from Contact.models import ContactUs

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
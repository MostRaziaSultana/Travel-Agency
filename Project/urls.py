from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Homepage.views import *
from Deals.admin import admin_site
from Deals.views import *
from Accounts.views import *
from Contact.views import *



urlpatterns = [
    path('admin/', admin_site.urls),
    path('shoily_admin/', admin.site.urls),
    path('', home, name='home'),
    path('gallery/', gallery, name='gallery'),
    path('destinations/', destinations, name='destinations'),
    path('tours/', tours, name='tours'),
    path('tour_details/<int:id>/', tour_details, name='tour_details'),
    path('bookings/<int:id>/', bookings, name='bookings'),

    path('registration/', registration, name='registration'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('contact/', contact, name='contact'),



]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
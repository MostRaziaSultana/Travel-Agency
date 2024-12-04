from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Homepage.views import *
from Deals.views import *
from Accounts.views import *
from Contact.views import *

from django.utils.translation import gettext_lazy as _



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('gallery/', gallery, name='gallery'),
    path('destinations/', destinations, name='destinations'),
    path('tours/', tours, name='tours'),
    path('tour_details/<int:id>/', tour_details, name='tour_details'),
    path('bookings/<int:id>/', bookings, name='bookings'),
    path('destination_details/<int:id>/', destination_details, name='destination_details'),
    path('bookings/payment/<int:booking_id>/', payment, name='payment'),
    path('success/<int:booking_id>/', success, name='success'),

    path('registration/', registration, name='registration'),
    path('login/', login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('contact/', contact, name='contact'),
    path('forgetpassword/', forgetpassword, name="forgetpassword"),
    path('change_password/<token>/', change_password, name="change_password"),



]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# # Change the admin site titles
# admin.site.site_header = _("Shoily")
# admin.site.index_title = _("Shoily")
# admin.site.site_title = _("Shoily")
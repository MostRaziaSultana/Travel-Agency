from django.db import models
from Accounts.models import User
import uuid
from ckeditor.fields import RichTextField

def generate_package_code():
    return f"PKG-{uuid.uuid4().hex[:8].upper()}"

class Package(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Sold Out', 'Sold Out'),
        ('Cancelled', 'Cancelled'),
    ]

    package_code = models.CharField(max_length=50, unique=True, default=generate_package_code)
    location = models.CharField(max_length=255)
    short_description = RichTextField()
    destination = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price per adult")
    child_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Price per child")
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='tours/', default='tours/default.jpg')
    bannerimage = models.ImageField(upload_to='tour_banners/', default='tour_banners/default.jpg',help_text="Banner image for the single tour")
    duration = models.CharField(max_length=50, null=True)
    overview = RichTextField(blank=True, null=True, help_text="Brief overview of the package")
    included = RichTextField(blank=True, null=True, help_text="What is included in this package")
    excluded = RichTextField(blank=True, null=True, help_text="What is excluded from this package")
    flight_details = models.CharField(max_length=100, blank=True, null=True,
                                               help_text="Airplane name with flight code")

    minimum_age = models.IntegerField(blank=True, null=True, help_text="Minimum age requirement for this package")
    departure_location = models.CharField(max_length=200, default='Departure location_Name')
    travel_direction = models.FileField(upload_to='downloads/pdfs/', blank=True, null=True,help_text="Upload pdf file")
    documentations = models.FileField(upload_to='downloads/pdfs/', blank=True, null=True, help_text="Upload pdf file")
    logo_assets = models.FileField(upload_to='downloads/pdfs/', blank=True, null=True, help_text="Upload pdf file")
    hot_deal = models.BooleanField(default=False,
                                           help_text="Select if this package should appear on hot deal part")
    show_on_homepage = models.BooleanField(default=False,
                                           help_text="Select if this package should appear on the homepage")


    class Meta:
        permissions = [
            ("can_crud_package", "Can CRUD Package"),
        ]

    def __str__(self):
        return self.location



class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Booked', 'Booked'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Refunded', 'Refunded'),
    ]

    TRAVEL_STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
    ]

    customer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    package_id = models.ForeignKey('Package', on_delete=models.CASCADE)
    booking_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES)
    travel_status = models.CharField(max_length=20, choices=TRAVEL_STATUS_CHOICES)
    price_at_booking = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=50,null=True)
    last_name = models.CharField(max_length=50,null=True)
    address_1 = models.CharField(max_length=255,null=True)
    address_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100,null=True)
    zip_code = models.CharField(max_length=20,null=True)
    adult = models.PositiveIntegerField(default=1)
    children =  models.PositiveIntegerField(default=0, blank=True, null=True)
    message = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"Booking {self.id} for {self.customer_id.username} - {self.package_id.destination}"


class Tour_page(models.Model):
    banner_image = models.ImageField(upload_to='tours/banners/', blank=True, null=True,
                                     help_text="Banner image for the tour page")
    discount = models.IntegerField(blank=True, null=True, help_text="Example: 25")
    discounted_destination_name = models.CharField(max_length=100, blank=True, null=True, help_text="Example: Srilanka")

    def __str__(self):
        return f"Tours Page - Discount: {self.discount}%"
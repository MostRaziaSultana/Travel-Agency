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
    tour_plan_description = RichTextField(blank=True, null=True,
                                          help_text="Detailed description of the tour plan")
    destination = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price per adult")
    child_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Price per child")
    offer = models.CharField(max_length=255, blank=True, null=True, help_text="Special offers for the package")
    total_seats = models.IntegerField()
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

    #
    # class Meta:
    #     permissions = [
    #         ("can_crud_package", "Can CRUD Package"),
    #     ]

    def __str__(self):
        return self.location



class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Booked', 'Booked'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]

    TRAVEL_STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
    ]

    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    package_id = models.ForeignKey('Package', on_delete=models.CASCADE)
    booking_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    travel_status = models.CharField(max_length=20, choices=TRAVEL_STATUS_CHOICES)
    price_at_booking = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    full_name = models.CharField(max_length=50,null=True)
    phone = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=255,null=True)
    email = models.EmailField(null=True)
    adult = models.PositiveIntegerField(default=1)
    children =  models.PositiveIntegerField(default=0, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    seen = models.BooleanField(default=False)


    def __str__(self):
        return f"Booking {self.id} for {self.creator} - {self.package_id.destination}"


class PaymentInfo(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('bkash', 'Bkash'),
        ('nagad', 'Nagad'),
        ('rocket', 'Rocket'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Refunded', 'Refunded'),
    ]
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="payments")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES,null=True)
    payment_type = models.CharField(max_length=20,choices=PAYMENT_TYPE_CHOICES)
    account_no = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    payment_date = models.DateField(null=True,blank=True)
    seen = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.payment_type} - {self.transaction_id}"

    class Meta:
        verbose_name = "Payment Info"
        verbose_name_plural = "Payment Info"


class Tour_page(models.Model):
    banner_image = models.ImageField(upload_to='tours/banners/', blank=True, null=True,
                                     help_text="Banner image for the tour page")
    discount = models.IntegerField(blank=True, null=True, help_text="Example: 25")
    discounted_destination_name = models.CharField(max_length=100, blank=True, null=True, help_text="Example: Srilanka")

    def __str__(self):
        return f"Tours Page - Discount: {self.discount}%"


class Destination(models.Model):
    YES_NO_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='destinations',default='destination name')
    image = models.ImageField(upload_to='destinations/images/', blank=True, null=True, default='destinations/images/default-image.jpg',
                              help_text="Image of the destination")
    description = RichTextField(help_text="Description of the destination")
    country_details = RichTextField(help_text="Describe Shortly about the country", null=True, blank=True, default="")

    # Country Details
    address = models.CharField(max_length=255, help_text="Address of the destination",null=True)
    visa_requirements = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='Yes',
                                         help_text="Visa requirements")
    languages_spoken = models.CharField(max_length=255, help_text="Languages spoken at destination",null=True)
    currency_used = models.CharField(max_length=100, help_text="Currency used in the country",null=True)
    distance = models.DecimalField(max_digits=10, decimal_places=1, help_text="Distance to the destination in meter",null=True)

    # Support and Emergency Details
    support_phone = models.CharField(max_length=20, help_text="Support phone number",null=True)
    emergency_email = models.EmailField(help_text="Emergency contact email",null=True)
    show_on_homepage = models.BooleanField(default=False, help_text="Show this destination on the homepage")

    def __str__(self):
        return self.package.destination


class PaymentDescription(models.Model):
    payment_description = RichTextField()

    def __str__(self):
        return f"Payment Details ID {self.id}"

    class Meta:
        verbose_name = "Payment Description"
        verbose_name_plural = "Payment Description"

from django.db import models
from Accounts.models import CustomUser as User
import uuid

def generate_package_code():
    return f"PKG-{uuid.uuid4().hex[:8].upper()}"

class Package(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Sold Out', 'Sold Out'),
        ('Cancelled', 'Cancelled'),
    ]

    package_code = models.CharField(max_length=50, unique=True, default=generate_package_code)
    package_name = models.CharField(max_length=255)
    description = models.TextField()  # Use a RichTextField if you are using a rich text editor
    destination = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_url = models.FileField(upload_to='package_images/', null=True)
    cancellation_policy = models.TextField(blank=True, null=True)
    additional_services = models.TextField(blank=True, null=True)

    class Meta:
        permissions = [
            ("can_crud_package", "Can CRUD Package"),
        ]

    def __str__(self):
        return self.package_name



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

    def __str__(self):
        return f"Booking {self.id} for {self.customer_id.username} - {self.package_id.package_name}"
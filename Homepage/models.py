from django.db import models
from Deals.models import Package
from ckeditor.fields import RichTextField

class Header(models.Model):
    logo = models.ImageField(upload_to='header/logo/', blank=True, null=True, default='default_images/default_logo.png')
    icon = models.ImageField(upload_to='header/icons/', blank=True, null=True,
                             default='default_images/default_icon.png')
    header_banner = models.ImageField(upload_to='header/banner/', blank=True, null=True,
                                      default='default_images/default_banner.jpg')
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class AboutSection(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image1 = models.ImageField(upload_to='about/')
    image2 = models.ImageField(upload_to='about/')
    list_item_1 = models.CharField(max_length=255)
    list_item_2 = models.CharField(max_length=255)
    list_item_3 = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Destinationinfo(models.Model):
    banner_image = models.ImageField(upload_to='destination_banner/')
    description = models.TextField(default="No description available.")

    class Meta:
        verbose_name = "Destination"
        verbose_name_plural = "Destinationinfo"


    def __str__(self):
        return self.description


class Destination(models.Model):
    YES_NO_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='destinations',default='destination name')
    image = models.ImageField(upload_to='destinations/images/', blank=True, null=True,
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



class FooterContent(models.Model):
    logo = models.ImageField(upload_to='footer_logos/')
    site_name = models.CharField(max_length=255,null=True)
    info_text = models.TextField()
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    copyright_year = models.PositiveIntegerField(null=True,blank=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    twitter = models.CharField(max_length=255, blank=True, null=True)
    youtube = models.CharField(max_length=255, blank=True, null=True)
    linkedin = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Footer Content - {self.site_name}"
    # class Meta:
    #     verbose_name = "Footer Info"
    #     verbose_name_plural = "Footer Info"


class FooterGalleryGroup(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Footer gallery group"
        verbose_name_plural = "Footer gallery groups"


class FooterGallery(models.Model):
    image = models.ImageField(upload_to='footer_gallery/')
    name = models.ForeignKey(FooterGalleryGroup, related_name='images', on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f'Image {self.id}'

    class Meta:
        verbose_name = "Footer gallery"
        verbose_name_plural = "Footer galleries"


class Gallery(models.Model):
    banner_image = models.ImageField(upload_to='gallery/')
    class Meta:
        verbose_name = "Gallery"
        verbose_name_plural = "Gallery images"
    def get_images(self):
        return GalleryImage.objects.filter(gallery=self)

    def __str__(self):
        return f'Gallery {self.id}'


class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='images', null=True)
    image = models.ImageField(upload_to='gallery/')

    def __str__(self):
        return f'Image {self.id} of Gallery {self.gallery.id}'
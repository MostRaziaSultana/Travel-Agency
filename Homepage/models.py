from django.db import models
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from datetime import date

class Header(models.Model):
    logo = models.ImageField(upload_to='header/logo/', blank=True, null=True, default='default_images/default_logo.png')
    favicon = models.ImageField(upload_to='header/icons/', blank=True, null=True,
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

def validate_year(value):
    current_year = date.today().year
    if value > current_year:
        raise ValidationError(f"The year {value} cannot be in the future.")
class FooterContent(models.Model):
    logo = models.ImageField(upload_to='footer_logos/')
    site_name = models.CharField(max_length=255,null=True)
    info_text = models.TextField()
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    copyright_year = models.PositiveIntegerField(default=date.today().year,null=True,blank=True,validators=[validate_year],help_text="Year for copyright (cannot be in the future).")
    instagram = models.CharField(max_length=255, blank=True, null=True)
    twitter = models.CharField(max_length=255, blank=True, null=True)
    youtube = models.CharField(max_length=255, blank=True, null=True)
    linkedin = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Footer Content - {self.site_name}"



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



class Banner(models.Model):

    login_banner = models.ImageField(upload_to='banners/login/', blank=True, null=True,
                                     verbose_name="Login Page Banner")
    registration_banner = models.ImageField(upload_to='banners/registration/', blank=True, null=True,
                                            verbose_name="Registration Page Banner")

    def __str__(self):
        return f"Banner ID {self.id}"





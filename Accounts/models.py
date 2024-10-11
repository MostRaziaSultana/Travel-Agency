from django.contrib.auth.models import AbstractUser, Permission
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    is_vendor = models.BooleanField(default=False)

    def is_staff_user(self):
        return self.is_staff and not self.is_superuser and not self.is_vendor

    def is_superadmin_user(self):
        return self.is_superuser

    def is_vendor_user(self):
        return self.is_vendor

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )



@receiver(post_save, sender=CustomUser)
def assign_vendor_permissions(sender, instance, created, **kwargs):
    if instance.is_vendor:
        permission = Permission.objects.get(codename='can_crud_package')
        instance.user_permissions.add(permission)
    else:
        permission = Permission.objects.get(codename='can_crud_package')
        instance.user_permissions.remove(permission)
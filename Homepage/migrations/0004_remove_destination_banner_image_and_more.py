# Generated by Django 5.1.2 on 2024-10-26 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Homepage', '0003_destination'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='destination',
            name='banner_image',
        ),
        migrations.RemoveField(
            model_name='destination',
            name='country',
        ),
    ]
# Generated by Django 5.1.2 on 2024-10-20 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Deals', '0012_package_departure_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='travel_direction',
            field=models.FileField(blank=True, help_text='Upload pdf file', null=True, upload_to='downloads/pdfs/'),
        ),
    ]

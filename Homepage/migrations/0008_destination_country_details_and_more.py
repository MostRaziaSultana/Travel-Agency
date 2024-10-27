# Generated by Django 5.1.2 on 2024-10-26 15:21

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Homepage', '0007_rename_location_destination_package'),
    ]

    operations = [
        migrations.AddField(
            model_name='destination',
            name='country_details',
            field=ckeditor.fields.RichTextField(blank=True, default='', help_text='Describe Shortly about the country', null=True),
        ),
        migrations.AlterField(
            model_name='destination',
            name='distance',
            field=models.DecimalField(decimal_places=1, help_text='Distance to the destination in meter', max_digits=10, null=True),
        ),
    ]
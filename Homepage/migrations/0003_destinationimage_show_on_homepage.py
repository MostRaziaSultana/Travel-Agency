# Generated by Django 5.1.2 on 2024-10-19 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Homepage', '0002_destinationimage_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='destinationimage',
            name='show_on_homepage',
            field=models.BooleanField(default=False, help_text='Select if this image should appear on the homepage'),
        ),
    ]
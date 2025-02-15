# Generated by Django 5.1.2 on 2024-10-27 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Deals', '0004_booking_adult_booking_children'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='child_price',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='Price per child', max_digits=10),
        ),
        migrations.AlterField(
            model_name='package',
            name='price',
            field=models.DecimalField(decimal_places=2, help_text='Price per adult', max_digits=10),
        ),
    ]

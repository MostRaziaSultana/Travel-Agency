# Generated by Django 5.1.2 on 2024-11-21 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Deals', '0014_remove_booking_payment_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentinfo',
            name='payment_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Paid', 'Paid'), ('Refunded', 'Refunded')], max_length=20, null=True),
        ),
    ]

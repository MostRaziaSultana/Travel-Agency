# Generated by Django 5.1.2 on 2024-11-21 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Deals', '0013_alter_paymentdescription_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='payment_status',
        ),
        migrations.AddField(
            model_name='paymentinfo',
            name='payment_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Paid', 'Paid'), ('Refunded', 'Refunded')], default='Pending', max_length=20),
        ),
    ]

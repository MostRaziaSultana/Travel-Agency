# Generated by Django 5.1.2 on 2024-11-21 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Deals', '0015_alter_paymentinfo_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentinfo',
            name='seen',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 5.1.2 on 2024-11-21 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Deals', '0016_paymentinfo_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='seen',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 5.1.2 on 2024-10-27 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Deals', '0003_remove_package_additional_services_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='adult',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='booking',
            name='children',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]

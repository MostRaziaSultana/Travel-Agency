# Generated by Django 5.1.2 on 2024-10-19 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Deals', '0003_rename_package_name_package_location_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tour_page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bannerimage', models.ImageField(blank=True, null=True, upload_to='tours_banners/')),
                ('offer', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]

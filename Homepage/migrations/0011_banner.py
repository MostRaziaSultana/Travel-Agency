# Generated by Django 5.1.2 on 2024-11-18 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Homepage', '0010_rename_icon_header_favicon'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_banner', models.ImageField(blank=True, null=True, upload_to='banners/login/', verbose_name='Login Page Banner')),
                ('registration_banner', models.ImageField(blank=True, null=True, upload_to='banners/registration/', verbose_name='Registration Page Banner')),
            ],
        ),
    ]
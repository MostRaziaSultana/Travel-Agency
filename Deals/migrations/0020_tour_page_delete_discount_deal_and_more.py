# Generated by Django 5.1.2 on 2024-10-20 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Deals', '0019_package_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tour_page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner_image', models.ImageField(blank=True, help_text='Banner image for the tour page', null=True, upload_to='tours/banners/')),
                ('discount', models.IntegerField(blank=True, help_text='Example: 25', null=True)),
                ('discounted_destination_name', models.CharField(blank=True, help_text='Example: Srilanka', max_length=100, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Discount_deal',
        ),
        migrations.AlterField(
            model_name='package',
            name='banner_image',
            field=models.ImageField(blank=True, help_text='Banner image for the single tour', null=True, upload_to='tours_details/banners/'),
        ),
    ]

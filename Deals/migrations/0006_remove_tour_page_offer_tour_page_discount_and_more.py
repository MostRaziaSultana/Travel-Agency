# Generated by Django 5.1.2 on 2024-10-19 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Deals', '0005_alter_tour_page_bannerimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tour_page',
            name='offer',
        ),
        migrations.AddField(
            model_name='tour_page',
            name='discount',
            field=models.IntegerField(blank=True, help_text='Example:25', null=True),
        ),
        migrations.AddField(
            model_name='tour_page',
            name='discounted_destination_name',
            field=models.CharField(blank=True, help_text='Example:Srilanka', max_length=100, null=True),
        ),
    ]

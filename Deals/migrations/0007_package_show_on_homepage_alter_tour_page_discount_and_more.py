# Generated by Django 5.1.2 on 2024-10-19 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Deals', '0006_remove_tour_page_offer_tour_page_discount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='show_on_homepage',
            field=models.BooleanField(default=False, help_text='Select if this package should appear on the homepage'),
        ),
        migrations.AlterField(
            model_name='tour_page',
            name='discount',
            field=models.IntegerField(blank=True, help_text='Example: 25', null=True),
        ),
        migrations.AlterField(
            model_name='tour_page',
            name='discounted_destination_name',
            field=models.CharField(blank=True, help_text='Example: Srilanka', max_length=100, null=True),
        ),
    ]
# Generated by Django 5.1.2 on 2024-10-20 06:19

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Deals', '0009_rename_description_package_short_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='minimum_age',
            field=models.IntegerField(blank=True, help_text='Minimum age requirement for this package', null=True),
        ),
        migrations.AlterField(
            model_name='package',
            name='additional_services',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='package',
            name='cancellation_policy',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='package',
            name='excluded',
            field=ckeditor.fields.RichTextField(blank=True, help_text='What is excluded from this package', null=True),
        ),
        migrations.AlterField(
            model_name='package',
            name='included',
            field=ckeditor.fields.RichTextField(blank=True, help_text='What is included in this package', null=True),
        ),
        migrations.AlterField(
            model_name='package',
            name='overview',
            field=ckeditor.fields.RichTextField(blank=True, help_text='Brief overview of the package', null=True),
        ),
        migrations.AlterField(
            model_name='package',
            name='short_description',
            field=ckeditor.fields.RichTextField(),
        ),
    ]

# Generated by Django 5.1.3 on 2024-12-03 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_website_websiteaddress_websiteemail_websitephone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aboutus',
            name='img',
        ),
        migrations.AddField(
            model_name='aboutus',
            name='imgs',
            field=models.ImageField(blank=True, null=True, upload_to='about_us-image'),
        ),
    ]

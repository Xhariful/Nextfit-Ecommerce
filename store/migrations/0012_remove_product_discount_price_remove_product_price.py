# Generated by Django 5.1.3 on 2024-12-18 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_variation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='discount_price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
    ]

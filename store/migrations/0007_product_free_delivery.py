# Generated by Django 5.1.3 on 2024-12-17 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_variation_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='free_delivery',
            field=models.BooleanField(default=False),
        ),
    ]

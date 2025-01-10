# Generated by Django 5.1.3 on 2024-12-18 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_rename_colour_color_alter_color_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variation',
            old_name='Color',
            new_name='color',
        ),
        migrations.AlterUniqueTogether(
            name='variation',
            unique_together={('product', 'size', 'color')},
        ),
    ]

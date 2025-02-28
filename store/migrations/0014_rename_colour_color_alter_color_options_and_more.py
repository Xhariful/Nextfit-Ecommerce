# Generated by Django 5.1.3 on 2024-12-18 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_product_parent_code'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Colour',
            new_name='Color',
        ),
        migrations.AlterModelOptions(
            name='color',
            options={'ordering': ['name'], 'verbose_name': 'Color', 'verbose_name_plural': 'Colors'},
        ),
        migrations.RenameField(
            model_name='variation',
            old_name='colour',
            new_name='Color',
        ),
        migrations.AlterUniqueTogether(
            name='variation',
            unique_together={('product', 'size', 'Color')},
        ),
    ]

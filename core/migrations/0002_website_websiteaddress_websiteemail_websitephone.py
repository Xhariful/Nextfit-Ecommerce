# Generated by Django 5.1.3 on 2024-12-02 07:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('logo', models.ImageField(upload_to='web-logo')),
                ('location', models.URLField(blank=True, max_length=30, null=True)),
                ('slug', models.SlugField()),
            ],
            options={
                'verbose_name': 'Website',
                'verbose_name_plural': 'Website',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='WebsiteAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField()),
                ('website', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='website_address', to='core.website')),
            ],
            options={
                'verbose_name': 'Website Address',
                'verbose_name_plural': 'Website addresses',
                'ordering': ['address'],
            },
        ),
        migrations.CreateModel(
            name='WebsiteEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('website', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='website_email', to='core.website')),
            ],
            options={
                'verbose_name': 'Website Email',
                'verbose_name_plural': 'Website Emails',
                'ordering': ['email'],
            },
        ),
        migrations.CreateModel(
            name='WebsitePhone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=30)),
                ('website', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='website_phone', to='core.website')),
            ],
            options={
                'verbose_name': 'Website Phone',
                'verbose_name_plural': 'Website Phones',
                'ordering': ['phone'],
            },
        ),
    ]

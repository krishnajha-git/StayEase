# Generated by Django 5.1.1 on 2024-10-22 03:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advertiser',
            fields=[
                ('advertiser_id', models.IntegerField(primary_key=True, serialize=False)),
                ('advertiser_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('address', models.TextField(max_length=300)),
                ('contact_details', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='PGOwner',
            fields=[
                ('owners_id', models.IntegerField(primary_key=True, serialize=False)),
                ('owners_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('contact_details', models.CharField(max_length=10)),
                ('aadhar_details', models.CharField(max_length=12, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('tenant_id', models.IntegerField(primary_key=True, serialize=False)),
                ('tenant_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('password', models.CharField(max_length=128)),
                ('category', models.CharField(choices=[('Student', 'Student'), ('Teacher', 'Teacher'), ('Nts', 'Non-Teaching Staff'), ('Hs', 'Housekeeping Staff')], max_length=20)),
                ('tenant_address', models.CharField(max_length=255)),
                ('tenant_dob', models.DateField()),
                ('contact_details', models.CharField(max_length=10)),
                ('course', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PostAd',
            fields=[
                ('ad_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('ads_for', models.CharField(choices=[('Need Roommate', 'Need Roommate'), ('Car Pooling', 'Car Pooling'), ('Lost & Found', 'Lost & Found'), ('News Updates', 'News Updates'), ('Event Tickets', 'Event Tickets'), ('Brand Promotion', 'Brand Promotion'), ('Social Campaign', 'Social Campaign'), ('Furniture Rentals', 'Furniture Rentals'), ('Academic Research', 'Academic Research'), ('More', 'More..')], max_length=50)),
                ('contact_details', models.CharField(max_length=255)),
                ('external_link', models.URLField(blank=True, null=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='ad_profile_images/')),
                ('description', models.TextField()),
                ('advertiser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.advertiser')),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField(max_length=3000)),
                ('single_room_count', models.IntegerField()),
                ('single_room_charges', models.DecimalField(decimal_places=2, max_digits=8)),
                ('double_room_count', models.IntegerField()),
                ('double_room_charges', models.DecimalField(decimal_places=2, max_digits=8)),
                ('triple_room_count', models.IntegerField()),
                ('triple_room_charges', models.DecimalField(decimal_places=2, max_digits=8)),
                ('n_room_count', models.IntegerField()),
                ('n_room_charges', models.DecimalField(decimal_places=2, max_digits=8)),
                ('wifi', models.BooleanField()),
                ('meals', models.BooleanField()),
                ('security', models.BooleanField()),
                ('ac', models.CharField(choices=[('AC', 'AC'), ('Non-AC', 'Non-AC')], max_length=10)),
                ('first_aid', models.BooleanField()),
                ('laundry_service', models.BooleanField()),
                ('house_keeping', models.BooleanField()),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='property_photos/profile/')),
                ('pg_photo_1', models.ImageField(blank=True, null=True, upload_to='property_photos/')),
                ('pg_photo_2', models.ImageField(blank=True, null=True, upload_to='property_photos/')),
                ('pg_photo_3', models.ImageField(blank=True, null=True, upload_to='property_photos/')),
                ('pg_photo_4', models.ImageField(blank=True, null=True, upload_to='property_photos/')),
                ('pgowner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='myapp.pgowner')),
            ],
        ),
    ]

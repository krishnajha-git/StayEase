from django.db import models

from django.db import models

# Tenant model
class Tenant(models.Model):
    CATEGORY_CHOICES = [
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Nts', 'Non-Teaching Staff'),
        ('Hs', 'Housekeeping Staff'),
    ]

    tenant_id = models.IntegerField(primary_key=True)
    tenant_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=128)  # Ensure password will be hashed in practice
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    tenant_address = models.CharField(max_length=255)
    tenant_dob = models.DateField()
    contact_details = models.CharField(max_length=10)
    course = models.CharField(max_length=50)

    def __str__(self):
        return self.tenant_name
# PG_Owner model
class PGOwner(models.Model):
    owners_id = models.IntegerField(primary_key=True)
    owners_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    contact_details = models.CharField(max_length=10)
    aadhar_details = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return self.owners_name

# Property model
from django.db import models

class Property(models.Model):
    id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=100)
    address = models.TextField(max_length=3000)

    pgowner = models.ForeignKey(PGOwner, on_delete=models.CASCADE, related_name='properties')  # Foreign key to PGOwner

    single_room_count = models.IntegerField()
    single_room_charges = models.DecimalField(max_digits=8, decimal_places=2)

    double_room_count = models.IntegerField()
    double_room_charges = models.DecimalField(max_digits=8, decimal_places=2)

    triple_room_count = models.IntegerField()
    triple_room_charges = models.DecimalField(max_digits=8, decimal_places=2)

    n_room_count = models.IntegerField()
    n_room_charges = models.DecimalField(max_digits=8, decimal_places=2)

    wifi = models.BooleanField()
    meals = models.BooleanField()
    security = models.BooleanField()
    ac = models.CharField(max_length=10, choices=[('AC', 'AC'), ('Non-AC', 'Non-AC')])
    first_aid = models.BooleanField()
    laundry_service = models.BooleanField()
    house_keeping = models.BooleanField()

    # Photo fields
    profile_photo = models.ImageField(upload_to='property_photos/profile/', null=True, blank=True)
    pg_photo_1 = models.ImageField(upload_to='property_photos/', null=True, blank=True)
    pg_photo_2 = models.ImageField(upload_to='property_photos/', null=True, blank=True)
    pg_photo_3 = models.ImageField(upload_to='property_photos/', null=True, blank=True)
    pg_photo_4 = models.ImageField(upload_to='property_photos/', null=True, blank=True)

    def __str__(self):
        return self.name




# Advertiser model
class Advertiser(models.Model):
    advertiser_id = models.IntegerField(primary_key=True)
    advertiser_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    address = models.TextField(max_length=300)
    contact_details = models.CharField(max_length=10)

    def __str__(self):
        return self.advertiser_name


from django.db import models

class PostAd(models.Model):
    AD_CHOICES = [
        ('Need Roommate', 'Need Roommate'),
        ('Car Pooling', 'Car Pooling'),
        ('Lost & Found', 'Lost & Found'),
        ('News Updates', 'News Updates'),
        ('Event Tickets', 'Event Tickets'),
        ('Brand Promotion', 'Brand Promotion'),
        ('Social Campaign', 'Social Campaign'),
        ('Furniture Rentals', 'Furniture Rentals'),
        ('Academic Research', 'Academic Research'),
        ('More', 'More..'),
    ]

    ad_id = models.IntegerField(unique=True,primary_key=True)
    ads_for = models.CharField(max_length=50, choices=AD_CHOICES)
    contact_details = models.CharField(max_length=255)
    external_link = models.URLField(max_length=200, blank=True, null=True)
    profile_image = models.ImageField(upload_to='ad_profile_images/', blank=True, null=True)
    description = models.TextField()
    
    # Foreign Key to Advertiser
    advertiser = models.ForeignKey('Advertiser', on_delete=models.CASCADE)

    def __str__(self):
        return f"Ad {self.ad_id} - {self.ads_for} by {self.advertiser.advertiser_name}"



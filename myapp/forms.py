from django import forms
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from datetime import timedelta, date
from .models import Tenant
import re
from django import forms
from django.core.exceptions import ValidationError
from .models import *
from django.contrib.auth.hashers import make_password


class TenantRegistrationForm(forms.ModelForm):
    tenant_id = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'TenantID', 'placeholder': 'Enter a unique ID'}),
        min_length=4,
        max_length=10
    )
    tenant_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'TenantName', 'placeholder': 'Enter your full name'}),
        max_length=50
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'Email', 'placeholder': 'Enter your email'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'Password', 'placeholder': 'Enter a strong password'}),
    )
    tenant_address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'TenantAddress', 'placeholder': 'Enter your address'}),
        max_length=255
    )
    tenant_dob = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'DateOfBirth', 'placeholder': 'Enter your date of birth', 'type': 'date'}),
    )
    contact_details = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'ContactDetails', 'placeholder': 'Enter your contact number'}),
        max_length=10
    )
    course = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'Course', 'placeholder': 'Enter your course/department'}),
        max_length=50
    )
    category = forms.ChoiceField(
        choices=Tenant.CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'Category'}),
    )

    class Meta:
        model = Tenant
        fields = ['tenant_id', 'tenant_name', 'email', 'password', 'tenant_address', 'tenant_dob', 'contact_details', 'course', 'category']

    def clean_tenant_id(self):
        tenant_id = self.cleaned_data.get('tenant_id')
        if len(tenant_id) < 4:
            raise forms.ValidationError("Tenant ID must be at least 4 digits.")
        if not tenant_id.isdigit():
            raise forms.ValidationError("Tenant ID must only contain digits.")
        if Tenant.objects.filter(tenant_id=tenant_id).exists():
            raise forms.ValidationError("Tenant ID already exists.")
        return tenant_id

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.match(r'^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z0-9_.!@#$%^&*()]{8,30}$', password):
            raise ValidationError("Password must contain at least one letter and one number.")
        return password

    def clean_contact_details(self):
        contact_details = self.cleaned_data.get('contact_details')
        if not contact_details.isdigit() or len(contact_details) != 10:
            raise ValidationError("Contact number must be 10 digits.")
        return contact_details



from django import forms
from .models import Property

class PropertyRegistrationForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'name', 
            'single_room_count', 
            'single_room_charges', 
            'double_room_count', 
            'double_room_charges', 
            'triple_room_count', 
            'triple_room_charges', 
            'n_room_count', 
            'n_room_charges', 
            'wifi', 
            'meals', 
            'security', 
            'ac', 
            'first_aid', 
            'laundry_service', 
            'house_keeping', 
            'profile_photo', 
            'pg_photo_1', 
            'pg_photo_2', 
            'pg_photo_3', 
            'pg_photo_4'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Property/PG Name', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'placeholder': 'Enter property address', 'rows': 4, 'class': 'form-control'}),
            'single_room_count': forms.NumberInput(attrs={'placeholder': 'No. of Single rooms', 'class': 'form-control'}),
            'single_room_charges': forms.NumberInput(attrs={'placeholder': 'Monthly charges for Single rooms', 'class': 'form-control'}),
            'double_room_count': forms.NumberInput(attrs={'placeholder': 'No. of Double rooms', 'class': 'form-control'}),
            'double_room_charges': forms.NumberInput(attrs={'placeholder': 'Monthly charges for Double rooms', 'class': 'form-control'}),
            'triple_room_count': forms.NumberInput(attrs={'placeholder': 'No. of Triple rooms', 'class': 'form-control'}),
            'triple_room_charges': forms.NumberInput(attrs={'placeholder': 'Monthly charges for Triple rooms', 'class': 'form-control'}),
            'n_room_count': forms.NumberInput(attrs={'placeholder': 'No. of N rooms', 'class': 'form-control'}),
            'n_room_charges': forms.NumberInput(attrs={'placeholder': 'Monthly charges for N rooms', 'class': 'form-control'}),
            'wifi': forms.Select(choices=[(True, 'Yes'), (False, 'No')], attrs={'class': 'form-control'}),
            'meals': forms.Select(choices=[(True, 'Yes'), (False, 'No')], attrs={'class': 'form-control'}),
            'security': forms.Select(choices=[(True, 'Yes'), (False, 'No')], attrs={'class': 'form-control'}),
            'ac': forms.Select(choices=[('AC', 'AC'), ('Non-AC', 'Non-AC')], attrs={'class': 'form-control'}),
            'first_aid': forms.Select(choices=[(True, 'Yes'), (False, 'No')], attrs={'class': 'form-control'}),
            'laundry_service': forms.Select(choices=[(True, 'Yes'), (False, 'No')], attrs={'class': 'form-control'}),
            'house_keeping': forms.Select(choices=[(True, 'Yes'), (False, 'No')], attrs={'class': 'form-control'}),
            'profile_photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'pg_photo_1': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'pg_photo_2': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'pg_photo_3': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'pg_photo_4': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        
    
    



class AdvertiserRegistrationForm(forms.ModelForm):
    advertiser_id = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'AdvertiserID', 'placeholder': 'Enter UserID'}),
        required=True
    )
    advertiser_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'AdvertiserName', 'placeholder': 'Enter Name'}),
        max_length=50,
        required=True
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'Email', 'placeholder': 'Enter Email'}),
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'Password', 'placeholder': 'Enter Password'}),
        required=True
    )
    contact_details = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'ContactDetails', 'placeholder': 'Enter Phone Number'}),
        max_length=10,
        required=True
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'Address', 'placeholder': 'Enter Address', 'rows': 4}),
        max_length=300,
        required=True
    )

    class Meta:
        model = Advertiser
        fields = ['advertiser_id', 'advertiser_name', 'email', 'password', 'contact_details', 'address']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.match(r'^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z0-9_.!@#$%^&*()]{8,30}$', password):
            raise ValidationError("Password must contain at least one letter and one number.")
        return password

    def clean_contact_details(self):
        contact_details = self.cleaned_data.get('contact_details')
        if not contact_details.isdigit() or len(contact_details) != 10:
            raise ValidationError("Contact number must be 10 digits.")
        return contact_details

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Advertiser.objects.filter(email=email).exists():
            raise ValidationError("Email is already registered.")
        return email

    def clean_advertiser_id(self):
        advertiser_id = self.cleaned_data.get('advertiser_id')
        if Advertiser.objects.filter(advertiser_id=advertiser_id).exists():
            raise ValidationError("Advertiser ID is already registered.")
        return advertiser_id



class PGOwnerRegistrationForm(forms.ModelForm):
    owners_id = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'OwnerID', 'placeholder': 'Enter your owner ID'}),
        max_length=20
    )
    owners_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'OwnerName', 'placeholder': 'Enter your full name'}),
        max_length=50
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'Email', 'placeholder': 'Enter your email'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'Password', 'placeholder': 'Enter a strong password'}),
    )
    contact_details = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'ContactDetails', 'placeholder': 'Enter your contact number'}),
        max_length=10
    )
    aadhar_details = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'AadharDetails', 'placeholder': 'Enter your 12-digit Aadhar number'}),
        max_length=12
    )

    class Meta:
        model = PGOwner
        fields = ['owners_id', 'owners_name', 'email', 'password', 'contact_details', 'aadhar_details']

    def clean_owners_id(self):
        owners_id = self.cleaned_data.get('owners_id')
        if len(owners_id) < 4:
            raise forms.ValidationError("Owner ID must be at least 4 digits.")
        if not owners_id.isdigit():
            raise forms.ValidationError("Owner ID must only contain digits.")
        if PGOwner.objects.filter(owners_id=owners_id).exists():
            raise forms.ValidationError("Owner ID already exists.")
        return owners_id

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not re.match(r'^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z0-9_.!@#$%^&*()]{8,30}$', password):
            raise forms.ValidationError("Password must contain at least one letter and one number.")
        return password

    def clean_contact_details(self):
        contact_details = self.cleaned_data.get('contact_details')
        if not contact_details.isdigit() or len(contact_details) != 10:
            raise forms.ValidationError("Contact number must be 10 digits.")
        return contact_details

    def clean_aadhar_details(self):
        aadhar_details = self.cleaned_data.get('aadhar_details')
        if not aadhar_details.isdigit() or len(aadhar_details) != 12:
            raise forms.ValidationError("Aadhar number must be exactly 12 digits.")
        return aadhar_details



class PostADRegistrationForm(forms.ModelForm):
    class Meta:
        model = PostAd
        fields = ['ad_id', 'ads_for', 'contact_details', 'external_link', 'profile_image', 'description']

        widgets = {
            'ad_id': forms.NumberInput(attrs={
                'placeholder': 'Enter your Ad ID number',
                'required': True
            }),
            'ads_for': forms.Select(attrs={
                'class': 'ads_for',
                'required': True
            }),
            'contact_details': forms.TextInput(attrs={
                'placeholder': 'Enter your contact details',
                'required': True
            }),
            'external_link': forms.URLInput(attrs={
                'placeholder': 'Add an external link',
                'required': True
            }),
            'profile_image': forms.FileInput(attrs={
                'accept': 'image/*'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Provide a brief description',
                'required': True
            }),
        }

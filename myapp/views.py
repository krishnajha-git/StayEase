from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.db import connection
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from .forms import *
from .models import *

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')
    connection.close()
    
class SelectView(View):
    def get(self, request):
        return render(request, 'select.html')
    connection.close()
    
   
class LoginView(View):
    def get(self, request):
        # Session management: Check if the user is already logged in and redirect them accordingly
        if "userID" in request.session:
            user_type = request.session.get("user_type")
            if user_type == "Tenant":
                return redirect('home_pg')  # Redirect Tenant
            elif user_type == "PGOwner":
                return redirect('home_property', owners_id=request.session.get('owners_id'))  # Redirect PG Owner
            elif user_type == "Advertiser":
                return redirect('home_myad', advertiser_id=request.session.get('advertiser_id'))  # Redirect Advertiser
        return render(request, 'login.html')

    def post(self, request):
        # Get user input from login form
        userID = request.POST.get('userID')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = None
        user_type = None

        if role == 'tenant':
            tenant = Tenant.objects.filter(tenant_id=userID).first()
            if tenant and check_password(password, tenant.password):
                user = tenant
                user_type = "Tenant"
            else:
                messages.error(request, "Invalid login for tenant.")
                return render(request, 'login.html')

        elif role == 'pg_owner':
            pg_owner = PGOwner.objects.filter(owners_id=userID).first()
            if not pg_owner:
                print(f"PG Owner not found with email {userID}")
                messages.error(request, "PG Owner with this UserID does not exist.")
            elif not check_password(password, pg_owner.password):  # Check hashed password
                print(f"Password entered: {password}")
                print(f"PG Owner's stored hashed password: {pg_owner.password}")
                messages.error(request, "Invalid password for PG Owner.")
            else:
                user = pg_owner
                user_type = "PGOwner"

        elif role == 'advertiser':
            advertiser = Advertiser.objects.filter(advertiser_id=userID).first()
            if not advertiser:
                print(f"Advertiser not found with email {userID}")
                messages.error(request, "Advertiser with this UserID does not exist.")
            elif not check_password(password, advertiser.password):  # Check hashed password
                print(f"Password entered: {password}")
                print(f"Advertiser's stored hashed password: {advertiser.password}")
                messages.error(request, "Invalid password for advertiser.")
            else:
                user = advertiser
                user_type = "Advertiser"

        if not user:
            messages.error(request, "Invalid login credentials.")
            return render(request, 'login.html')

        request.session['userID'] = userID
        request.session['user_type'] = user_type

        if user_type == "Tenant":
            messages.success(request, "Welcome, Tenant!")
            return redirect('home_pg')
        elif user_type == "PGOwner":
            request.session['owners_id'] = user.owners_id
            messages.success(request, "Welcome, PG Owner!")
            return redirect('home_property', owners_id=user.owners_id)
        elif user_type == "Advertiser":
            request.session['advertiser_id'] = user.advertiser_id
            messages.success(request, "Welcome, Advertiser!")
            return redirect('home_myad', advertiser_id=user.advertiser_id)


class LogoutView(View):
    def post(self, request):
        auth_logout(request)
        return redirect('login')

    
class NoticeView(View):
    def get(self, request):
        return render(request, 'notice.html')

class Home_PropertyView(View):
    @method_decorator(never_cache)
    def get(self, request, owners_id, *args, **kwargs):
        # Check if user is logged in
        if "userID" not in request.session:
            return redirect('login')  # Redirect to login if not logged in
        
        # Fetch the PGOwner instance based on the owners_id
        try:
            owner = PGOwner.objects.get(owners_id=owners_id)
        except PGOwner.DoesNotExist:
            return render(request, 'error.html', {'message': 'Owner not found'})
        
        # Fetch all properties related to the owner
        properties = Property.objects.filter(pgowner=owner)
        
        # Render the properties in the template
        return render(request, 'home_property.html', {
            'properties': properties,
            'owners_id': owners_id,
            'owner_name': owner.owners_name,  # Make sure to replace with the actual field name for the owner's name
        })
        
class ComparePropertiesView(View):
    def get(self, request):
        # Fetch all properties
        properties = Property.objects.all()

        # Render the compare template with the properties
        return render(request, 'compare.html', {
            'properties': properties,
        })
        
class StayView(View):
    def get(self, request, property_id):
        # Fetch the specific property or return a 404 error if not found
        property = get_object_or_404(Property, id=property_id)

        # Render the stay template with the property details
        return render(request, 'stay.html', {
            'property': property,
        })
        
from django.views.generic.detail import DetailView
class GalleryPageView(DetailView):
    model = Property
    template_name = 'gallery_page.html'
    context_object_name = 'property'

    # Optionally, you can override `get_context_data` if you want to add extra context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add extra context if needed
        return context

class Home_MYADView(View):
    @method_decorator(never_cache)
    def get(self, request, advertiser_id):
        # Check if user is logged in
        if "userID" not in request.session:
            return redirect('login')  # Redirect to login if not logged in

        # Fetch the advertiser
        try:
            advertiser = Advertiser.objects.get(advertiser_id=advertiser_id)
        except Advertiser.DoesNotExist:
            return render(request, 'home_myad.html', {'ads': [], 'advertiser_id': advertiser_id, 'advertiser_name': None})

        # Fetch all advertisements for the specific advertiser
        ads = PostAd.objects.filter(advertiser=advertiser)

        # Prepare context with advertisements and advertiser info
        context = {
            'ads': ads,
            'advertiser_id': advertiser.advertiser_id,
            'advertiser_name': advertiser.advertiser_name,  # Add advertiser name to context
        }
        return render(request, 'home_myad.html', context)


class Home_PGView(View):
    @method_decorator(never_cache)
    def get(self, request):
        if "userID" not in request.session:
            return redirect('login')  # Redirect to login if not logged in
        
        # Fetch all properties from the database
        properties = Property.objects.all()
        context = {
            'properties': properties,
        }
        return render(request, 'home_pg.html', context)

from django.shortcuts import render
from .models import PostAd

class Home_ADSView(View):
    def get(self, request):
        # Fetch all ads from the PostAd model
        ads = PostAd.objects.all()
        return render(request, 'home_ads.html', {'ads': ads})

class Selected_ADView(View):
    def get(self, request):
        # Get the selected category from the query string (e.g., ?category=Lost)
        category = request.GET.get('category', None)

        # Fetch ads filtered by the selected category, ignoring case
        ads = PostAd.objects.filter(ads_for__iexact=category) if category else PostAd.objects.all()

        # Render the selected ads in the template, pass ads and category for display
        return render(request, 'selected_ad.html', {'ads': ads, 'category': category})



class ChooseView(View):
    def get(self, request):
        return render(request, 'choose.html')

    def post(self, request):
        # Get the selected role from the dropdown
        selected_role = request.POST.get('role')

        # Redirect based on the selected role
        if selected_role == 'tenant':
            return redirect('register_tenant')  # URL name for 'register_tenant.html'
        elif selected_role == 'pg_owner':
            return redirect('register_pgowner')  # URL name for 'pgowner_tenant.html'
        elif selected_role == 'advertiser':
            return redirect('register_advertiser')  # URL name for 'advertiser_tenant.html'
        else:
            # If no valid role is selected, reload the page with an error message
            return render(request, 'choose.html', {'error': 'Please select a valid role.'})


class TenantRegisterView(View):
    def get(self, request):
        form = TenantRegistrationForm()
        return render(request, 'register_tenant.html', {'form': form})

    def post(self, request):
        form = TenantRegistrationForm(request.POST)
        if form.is_valid():
            tenant_id = form.cleaned_data['tenant_id']
            tenant_name = form.cleaned_data['tenant_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']  # Original password
            category = form.cleaned_data['category']
            tenant_address = form.cleaned_data['tenant_address']
            tenant_dob = form.cleaned_data['tenant_dob']
            contact_details = form.cleaned_data['contact_details']
            course = form.cleaned_data['course']

            # Check if tenant_id, tenant name or email already exists
            if Tenant.objects.filter(tenant_id=tenant_id).exists():
                messages.error(request, "Tenant ID already exists")
                return redirect('tenant_register')

            if Tenant.objects.filter(tenant_name=tenant_name).exists():
                messages.error(request, "Username already taken")
                return redirect('tenant_register')

            if Tenant.objects.filter(email=email).exists():
                messages.error(request, "Email already registered")
                return redirect('tenant_register')

            # Create new tenant with hashed password
            Tenant.objects.create(
                tenant_id=tenant_id,
                tenant_name=tenant_name,
                email=email,
                password=make_password(password),  # Hash the password before saving
                category=category,
                tenant_address=tenant_address,
                tenant_dob=tenant_dob,
                contact_details=contact_details,
                course=course
            )

            messages.success(request, "Registration successful")
            return redirect('login')

        else:
            for error in form.errors.values():
                messages.error(request, error)
            return render(request, 'register_tenant.html', {'form': form})
    connection.close()

 

from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib import messages
from .models import PGOwner, Property  # Import your models
from .forms import PropertyRegistrationForm  # Import your form

from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import PropertyRegistrationForm
from .models import PGOwner

class PropertyRegisterView(View):
    def get(self, request, owners_id):
        # Check if the owner is in session
        if "owners_id" not in request.session:
            # If not in session, redirect to login or another relevant page
            return redirect('login')  # or wherever you want non-logged-in users to go

        # Display the property registration form
        form = PropertyRegistrationForm()
        return render(request, 'register_property.html', {'form': form, 'owners_id': owners_id})

    def post(self, request, owners_id):
        print(request.POST)  # Check if all form data is being posted
        print(request.FILES)  # Check the uploaded files
        form = PropertyRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            pgowner = get_object_or_404(PGOwner, owners_id=owners_id)

            # Create a new property object and assign the PGOwner foreign key
            new_property = form.save(commit=False)
            new_property.pgowner = pgowner

            # Handle multiple file uploads for PG photos
            pg_photos = request.FILES.getlist('pg_photos')
            for i, photo in enumerate(pg_photos):
                if i < 4:  # Ensure only the first four photos are saved
                    setattr(new_property, f'pg_photo_{i + 1}', photo)

            new_property.save()

            messages.success(request, "Property registration successful")

            # Redirect to the home_property view after successful registration
            return redirect('home_property', owners_id=owners_id)
        else:
            print(form.errors)  # Print all form errors for debugging
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")  # Show specific field error

            return render(request, 'register_property.html', {'form': form, 'owners_id': owners_id})




class AdvertiserRegisterView(View):
    def get(self, request):
        if "advertiser_name" in request.session:
            return redirect('home')

        form = AdvertiserRegistrationForm()
        return render(request, 'register_advertiser.html', {'form': form})

    def post(self, request):
        form = AdvertiserRegistrationForm(request.POST)
        if form.is_valid():
            advertiser_id = form.cleaned_data['advertiser_id']
            advertiser_name = form.cleaned_data['advertiser_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            contact_details = form.cleaned_data['contact_details']
            address = form.cleaned_data['address']

            # Ensure that the advertiser_id is not already taken
            if Advertiser.objects.filter(advertiser_id=advertiser_id).exists():
                messages.error(request, "Advertiser ID already taken")
                return render(request, 'register_advertiser.html', {'form': form})

            if Advertiser.objects.filter(email=email).exists():
                messages.error(request, "Email already registered")
                return render(request, 'register_advertiser.html', {'form': form})

            # Create new advertiser and save to database
            new_advertiser = Advertiser(
                advertiser_id=advertiser_id,
                advertiser_name=advertiser_name,
                email=email,
                password=make_password(password),  # Hashing the password before saving
                contact_details=contact_details,
                address=address,
            )
            new_advertiser.save()

            # Registration success
            messages.success(request, "Registration successful")
            return redirect('login')

        else:
            # Handle errors and re-render the form with error messages
            for error in form.errors.values():
                messages.error(request, error)
            return render(request, 'register_advertiser.html', {'form': form})



class PGOwnerRegisterView(View):
    def get(self, request):
        if "owners_name" in request.session:
            return redirect('home')

        form = PGOwnerRegistrationForm()
        return render(request, 'register_pgowner.html', {'form': form})

    def post(self, request):
        form = PGOwnerRegistrationForm(request.POST)
        if form.is_valid():
            owners_id = form.cleaned_data['owners_id']
            owners_name = form.cleaned_data['owners_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            contact_details = form.cleaned_data['contact_details']
            aadhar_details = form.cleaned_data['aadhar_details']

            # Check if the ID or email already exists
            if PGOwner.objects.filter(owners_id=owners_id).exists():
                messages.error(request, "Owner ID already taken")
                return redirect('register_pgowner')

            if PGOwner.objects.filter(owners_name=owners_name).exists():
                messages.error(request, "Owner name already taken")
                return redirect('register_pgowner')

            if PGOwner.objects.filter(email=email).exists():
                messages.error(request, "Email already registered")
                return redirect('register_pgowner')

            new_pgowner = PGOwner(
                owners_id=owners_id,
                owners_name=owners_name,
                email=email,
                password=make_password(password),
                contact_details=contact_details,
                aadhar_details=aadhar_details
            )
            new_pgowner.save()

            messages.success(request, "Registration successful")
            return redirect('login')  # Redirecting to login.html after successful registration

        else:
            for error in form.errors.values():
                messages.error(request, error)
            return render(request, 'register_pgowner.html', {'form': form})

class PostADView(View):
    def get(self, request, advertiser_id):
        form = PostADRegistrationForm()
        return render(request, 'post_ad.html', {'form': form, 'advertiser_id': advertiser_id})

    def post(self, request, advertiser_id):
        form = PostADRegistrationForm(request.POST, request.FILES)  # Include request.FILES for file uploads
        if form.is_valid():
            post_ad = form.save(commit=False)
            post_ad.advertiser_id = advertiser_id
            post_ad.external_link = form.cleaned_data['external_link']  # Ensure external link is processed
            post_ad.save()
            return redirect('home_myad', advertiser_id=advertiser_id)
        return render(request, 'post_ad.html', {'form': form, 'advertiser_id': advertiser_id})

class DeleteAdView(View):
    def delete(self, request, ad_id):
        try:
            # Find the ad by ID and delete it
            ad = PostAd.objects.get(ad_id=ad_id)
            ad.delete()
            return JsonResponse({'status': 'success'})
        except PostAd.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Ad not found'}, status=404)
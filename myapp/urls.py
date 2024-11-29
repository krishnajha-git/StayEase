from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('select/', SelectView.as_view(), name='select'),
    path('choose/', ChooseView.as_view(), name='choose'),
    path('notice/', NoticeView.as_view(), name='notice'),
    path('home_pg/', Home_PGView.as_view(), name='home_pg'),
    path('home_ads/', Home_ADSView.as_view(), name='home_ads'),
    path('post_ad/<int:advertiser_id>/', PostADView.as_view(), name='post_ad'),
    path('home_myad/<int:advertiser_id>/', Home_MYADView.as_view(), name='home_myad'),  
    path('home_property/<int:owners_id>/', Home_PropertyView.as_view(), name='home_property'),
    path('tenant/register/', TenantRegisterView.as_view(), name='tenant_register'),
    path('pg_owner/register/', PGOwnerRegisterView.as_view(), name='register_pgowner'),
    path('property/register/<str:owners_id>/', PropertyRegisterView.as_view(), name='register_property'),
    path('advertiser/register/', AdvertiserRegisterView.as_view(), name='register_advertiser'),
    path('delete_ad/<int:ad_id>/', DeleteAdView.as_view(), name='delete_ad'),
    path('selected-ad/', Selected_ADView.as_view(), name='selected_ad'),
    path('compare/', ComparePropertiesView.as_view(), name='compare_properties'),
    path('stay/<int:property_id>/', StayView.as_view(), name='stay'),
    path('gallery/<int:pk>/', GalleryPageView.as_view(), name='gallery_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
urlpatterns += staticfiles_urlpatterns()

print("URL patterns loaded correctly")
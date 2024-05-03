"""
URL configuration for skipskid project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from carrier import views as carrierviews
from shipper import views as shipperviews

from django.contrib.auth import views as auth_views

from skipskid.views import shipping_home, carrier_home, why_silyatrans, carrier_page

admin.site.enable_nav_sidebar = False

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', shipping_home, name='shipping_home'),
    path('carrier/signup/', carrierviews.Carriersignup, name='Carriersignup'),
    path('carrier/login/', carrierviews.Carrierlogin, name='Carrierlogin'),
    path('carrier/home/', carrierviews.Carrierhome, name='Carrierhome'),
    path('carrier/logout/', carrierviews.Carrierlogout, name='Carrierlogout'),
    path('carrier/accountsettings/', carrierviews.accountsettings, name='accountsettings'),
    path('carrier/beforesignup/',carrierviews.beforesignup, name="beforesignup"),

    path('shipper/signup/', shipperviews.signup, name='Shippersignup'),
    path('shipper/login/', shipperviews.Shipperlogin, name='Shipperlogin'),
    path('shipper/home/', shipperviews.home, name='Shipperhome'),
    path('shipper/logout/', shipperviews.logout, name='Shipperlogout'),
    path('shipper/accountsettings/', shipperviews.accountsettings, name='accountsettings'),
    path('shipper/beforesignup/',shipperviews.beforesignup, name="beforesignup"),

    path('reset_password', auth_views.PasswordResetView.as_view(), name= 'reset_password'),
    path('reset_password_done', auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), name='password_reset_done'),
    path('reset_password_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),


    path('shipping/', shipping_home, name='shipping_home'),
    path('shipping/carrier/', carrier_home, name='carrier_home'),
    path('carrier/silyatrans/', why_silyatrans, name='why_trans'),

    path('carrier/', carrier_page, name = 'carrier_page')



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Carrier, CarrierAddress, CarrierVehicle, CarrierEquipment, Certification, CarrierCertification






# Register your models here.
admin.site.register(Certification)


class CarrierAddressInline(admin.StackedInline):
    model = CarrierAddress
    verbose_name = "Address"
    icon = "location_on"
    fields = (
        ("line1", "line2"),
        ("city", "state"), "postcode"
    )
    '''
    no need for has_add_permission because of default_permissions set to False
    for all users
    '''

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class CarrierEquipmentInline(admin.TabularInline):
    model = CarrierEquipment
    verbose_name = "Equipments"
    icon = "pallet"
    extra = 0

    '''
    no need for has_add_permission because of default_permissions set to False
    for all users
    '''

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class CarrierVehicleInline(admin.TabularInline):
    model = CarrierVehicle
    verbose_name = "Vehicles"
    icon = "local_shipping"
    extra = 0

    '''
    no need for has_add_permission because of default_permissions set to False
    for all users
    '''

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class CarrierCertificationInline(admin.TabularInline):
    model = CarrierCertification
    verbose_name = "Certifications"
    icon = "workspace_premium"
    extra = 0

    '''
    no need for has_add_permission because of default_permissions set to False
    for all users
    '''

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(Carrier)
class CarrierAdmin(admin.ModelAdmin):

    search_fields = ("name", "contact_person")
    list_filter = ("address__postcode", "address__state", "vehicles__type", "equipments__type", "pounds_plus", "miles_plus")
    list_display = ("name", "contact_person", "phone_number", "email","password", "get_address", "num_vehicles", "reference",'is_staff', 'is_active','is_superuser')
    fields = (
        ("name", "about"),
        ("contact_person", "reference"),
        ("email", "password"),
        "phone_number",
        "miles_plus",
        "pounds_plus",
        "is_staff", "is_active", "is_superuser"
    )
    radio_fields = {'pounds_plus': admin.HORIZONTAL, 'miles_plus': admin.HORIZONTAL}
    readonly_fields = ("reference",)

    @admin.display(description=_("Address"))
    def get_address(self, instance, **kwargs):
        return instance.address.summary

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("equipments", "vehicles")

    '''
    no need for has_add_permission because of default_permissions set to False
    for all users
    '''

    def has_add_permission(self, request):
        return True#False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    inlines = [CarrierAddressInline, CarrierVehicleInline, CarrierEquipmentInline, CarrierCertificationInline]

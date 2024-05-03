from django.contrib import admin
from django import forms
from .models import Shipper, Business, Individual, BusinessAddress, IndividualAddress, TypeOfIndustry
                #  IndividualPreferredCarrier, ShipperEquipment, IndividualDelivery
from django.utils.translation import gettext_lazy as _

from django.contrib import admin
from.models import Shipper, Business, Individual

admin.site.register(TypeOfIndustry)

class BusinessAddressInline(admin.StackedInline):
    model = BusinessAddress
    verbose_name = "_Address"
    icon = "location_on"
    fields = (
        ("line1", "line2"),
        ("city", "state"), "postcode"
    )
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    verbose_name_plural = "_Addresses"


class IndividualAddressInline(admin.StackedInline):
    model = IndividualAddress
    verbose_name = "_Address"
    icon = "location_on"
    fields = (
        ("line1", "line2"),
        ("city", "state"), "postcode"
    )
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    verbose_name_plural = "_Addresses"

class TypeOfIndustryInline(admin.TabularInline):
    model = TypeOfIndustry
    verbose_name = "Type of Industry"
    verbose_name_plural = "Types of Industry"
    # icon =
    extra = 0
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class BusinessInline(admin.StackedInline):
    model = Business
    fields = ['type_of_industry', 'contact_person', 'website', 'image', 'has_loading_dock', 'has_forklift', 'has_ramp']
    list_display = ("name", "email_address", "phone_number", "type_of_industry", "address", "zip_code")
    verbose_name = "Business"
    verbose_name_plural = "Businesses"
    icon = "business"
    inlines = [BusinessAddressInline]
    


class IndividualInline(admin.StackedInline):
    model = Individual
    can_delete = False
    fields = ['parking_available', 'easy_access_to_loading']
    verbose_name = "Individual"
    verbose_name_plural = "Individuals"
    inlines = [IndividualAddressInline]


@admin.register(Shipper)
class ShipperAdmin(admin.ModelAdmin):
    inlines = (BusinessInline, IndividualInline)
    search_fields = ("name", "contact_person")
    list_filter = ("addresses__postcode", "addresses__state")
    list_display = ("name", "phone_number", "email_address")
    fields = (
        ("name"),
        ("email_address", "phone_number")
    )

admin.site.register(Business)
admin.site.register(Individual)
admin.site.register(BusinessAddress)
admin.site.register(IndividualAddress)
from django.contrib import admin
from .models import Business, BusinessAddress, BusinessTypeOfIndustry, ShipperEquipment
from django.utils.translation import gettext_lazy as _


class BusinessAddressInline(admin.StackedInline):
    model = BusinessAddress
    verbose_name = "Address"
    icon = "location_on"
    fields = (
        ("line1", "line2"),
        ("city", "state"), 
        "postcode"
    )
    """
    no need for has_add_permission because of default_permissions set to False
    for all users
    """

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class BusinessTypeOfIndustryInline(admin.TabularInline):
    model = BusinessTypeOfIndustry
    verbose_name = "Typeofindustry"
    icon = "factory"
    extra = 0

    """
    no need for has_add_permission because of default_permissions set to False
    for all users
    """

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
    


class ShipperEquipmentInline(admin.StackedInline):
    model = ShipperEquipment
    verbose_name = "ShipperEquipment"
    icon = "Forklift"
    extra = 0
    """
    no need for has_add_permission because of default_permissions set to False
    for all users
    """

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


# @admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):

    search_fields = ('business_name', 'contact_person', 'business_phone')
    list_filter = ("address__postcode", "address__state", "Type_of_industries__TypeOfIndustry", "equipments__type")

    list_display = ("business_name", "contact_person","business_email", "business_phone", "reference", "website", "has_loading_dock", "has_forklift", "has_ramp", "display_image")
    fieldsets = [
        (
            None,
            {
                "fields": [("business_name", "contact_person"),("business_email", "website"), "image"],
            },
        ),
    ]
    radio_fields = {"has_loading_dock": admin.HORIZONTAL, "has_forklift": admin.HORIZONTAL, "has_ramp": admin.HORIZONTAL}
    readonly_fields = ("reference",)

    @admin.display(description=_("Address"))
    def get_address(self, instance, **kwargs):
        return instance.address.summary if instance.address else ""
    
    @admin.display(description=_("Image"))
    def display_image(self, instance):
        return instance.image.url if instance.image else "No image"
    display_image.short_description = "Image"

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("equipments", "Type_of_industries__TypeOfIndustry", "address")

    def has_add_permission(self, request):
        return True #False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    inlines = [BusinessAddressInline, BusinessTypeOfIndustryInline, ShipperEquipmentInline]




admin.site.register(Business)



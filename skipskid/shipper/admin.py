from django.contrib import admin
from .models import Business, Individual, BusinessAddress, IndividualAddress, BusinessTypeOfIndustry, IndividualPreferredCarrier, ShipperEquipment, IndividualDelivery
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

class IndividualAddressInline(admin.StackedInline):
    model = IndividualAddress
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
    
class PreferredCarrierInline(admin.StackedInline):
    model = IndividualPreferredCarrier
    verbose_name = "PreferredCarrier"
    icon = "PreferredCarrier"
    extra = 0
    """
    no need for has_add_permission because of default_permissions set to False
    for all users
    """

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
class IndividualDeliveryInline(admin.StackedInline):
    model = IndividualDelivery
    verbose_name = "IndividualDelivery"
    icon = "IndividualDelivery"
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


# @admin.register(Individual)
class IndividualAdmin(admin.ModelAdmin):

    search_fields = ('first_name', 'email', 'phone')
    list_filter = ("address__postcode", "address__state", "preferred_carriers__carrier")

    list_display = ("first_name", "email", "phone", "zip_code", "get_address", "reference", "easy_access_to_loading", "parking_available")
    fieldsets = [
        (
            None,
            {
                "fields": [("first_name", "email"), ("phone", "zip_code"), "get_address"],
            },
        ),
    ]
    radio_fields = {"easy_access_to_loading": admin.HORIZONTAL, "parking_available": admin.HORIZONTAL}
    readonly_fields = ("reference",)

    @admin.display(description=_("Address"))
    def get_address(self, instance, **kwargs):
        return instance.address.summary
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("preferred_carriers", "address")

    def has_add_permission(self, request):
        return True #False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    inlines = [IndividualAddressInline, PreferredCarrierInline, IndividualDeliveryInline]



admin.site.register(Business)
admin.site.register(Individual)

# admin.site.register(PreferredCarrier, PreferredCarrierAdmin)
# admin.site.register(IndividualDelivery, IndividualDeliveryAdmin)
# admin.site.register(Business, BusinessAdmin)
















# class PastDeliveryAdmin(admin.ModelAdmin):
#     list_display = ['get_business_name', 'delivery_date']
#     search_fields = ['shipper__business_name', 'delivery_date']

#     def get_business_name(self, obj):
#         return obj.shipper.business_name

#     get_business_name.admin_order_field = 'shipper__business_name'

# class ShipperEquipmentAdmin(admin.ModelAdmin):
#     list_display = ['business_name', 'type', 'number']
#     search_fields = ['shipper__business_name', 'type__name']


# admin.site.register(PastDelivery, PastDeliveryAdmin)
#admin.site.register(ShipperEquipmentAdmin, ShipperEquipmentAdmin)

















# from django.contrib import admin
# from shipper.models.individual import Individual, PreferredCarrier, IndividualDelivery
# from shipper.models.business import Business, PastDelivery

# class IndividualAdmin(admin.ModelAdmin):
#     list_display = ['first_name', 'home_zip_code', 'email', 'phone', 'parking_available', 'easy_access_to_loading']
#     search_fields = ['first_name', 'home_zip_code', 'email', 'phone']

# class PreferredCarrierAdmin(admin.ModelAdmin):
#     list_display = ['individual', 'carrier']
#     search_fields = ['individual__first_name', 'carrier__name']

# class IndividualDeliveryAdmin(admin.ModelAdmin):
#     list_display = ['individual', 'origin', 'destination', 'status', 'pickup_date', 'delivery_date', 'assigned_carrier', 'offers']
#     search_fields = ['individual__first_name', 'origin', 'destination']

# class BusinessAdmin(admin.ModelAdmin):
#     list_display = ['business_name', 'address', 'type_of_industry', 'contact_person', 'business_email', 'business_phone', 'website']
#     search_fields = ['business_name',  'contact_person', 'business_email', 'business_phone']

# class PastDeliveryAdmin(admin.ModelAdmin):
#     list_display = ['get_business_name', 'delivery_date']
#     search_fields = ['shipper__business_name', 'delivery_date']

#     def get_business_name(self, obj):
#         return obj.shipper.business_name

#     get_business_name.admin_order_field = 'shipper__business_name'

# #a modifier
# class ShipperEquipmentAdmin(admin.ModelAdmin):
#     list_display = ['business_name', 'type', 'number']
#     search_fields = ['shipper__business_name', 'type__name']

# admin.site.register(Individual, IndividualAdmin)
# admin.site.register(PreferredCarrier, PreferredCarrierAdmin)
# admin.site.register(IndividualDelivery, IndividualDeliveryAdmin)
# admin.site.register(Business, BusinessAdmin)
# admin.site.register(PastDelivery, PastDeliveryAdmin)






# admin.site.register(ShipperEquipmentAdmin, ShipperEquipmentAdmin)


# from django.contrib import admin
# from django.utils.translation import gettext_lazy as _
# from .models import Shipper, PastDelivery

# from .models import Shipper, PastDelivery, ShipperEquipment

# @admin.register(Shipper)
# class ShipperAdmin(admin.ModelAdmin):
#     list_display = ["business_name", "type_of_industry", "contact_person", "business_email", "business_phone", "get_equipment_type"]
#     search_fields = ["business_name", "type_of_industry", "contact_person", "business_email"]
#     ordering = ["business_name"]

#     @admin.display(description=_("Address"))
#     def get_address(self, instance, **kwargs):
#         return instance.address.summary

#     @admin.display(description=_("Equipment Type"))
#     def get_equipment_type(self, instance):
#         # Assuming a Shipper can have multiple equipments, you might want to concatenate or format the types
#         equipment_types = instance.equipments.all().values_list('type__name', flat=True)
#         return ", ".join(equipment_types)


#     def get_queryset(self, request):
#         return super().get_queryset(request).prefetch_related("equipments")

#     """
#     no need for has_add_permission because of default_permissions set to False
#     for all users
#     """

#     def has_add_permission(self, request):
#         return True

#     def has_change_permission(self, request, obj=None):
#         return True

#     def has_delete_permission(self, request, obj=None):
#         return True

# @admin.register(PastDelivery)
# class PastDeliveryAdmin(admin.ModelAdmin):
#     list_display = ["shipper", "delivery_date"]
#     search_fields = ["shipper__business_name"]
#     ordering = ["-delivery_date"]

#     def has_add_permission(self, request):
#         return True

#     def has_change_permission(self, request, obj=None):
#         return True

#     def has_delete_permission(self, request, obj=None):
#         return True


# class ShipperEquipmentInline(admin.TabularInline):
#     model = ShipperEquipment
#     verbose_name = "Equipment"
#     extra = 0
    

















    
# from django.contrib import admin

# from .models import Shipper

# # Register your models here.


# # admin.site.register(Shipper)

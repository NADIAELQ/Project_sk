from django.contrib import admin
from .models import Individual, IndividualAddress, IndividualPreferredCarrier, IndividualDelivery
from django.utils.translation import gettext_lazy as _



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


    
class PreferredCarrierInline(admin.StackedInline):
    model = IndividualPreferredCarrier
    verbose_name = "PreferredCarrier"
    icon = "local_shipping"
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



@admin.register(Individual)
class IndividualAdmin(admin.ModelAdmin):

    search_fields = ('first_name', 'email', 'phone')
    list_filter = ("address__postcode", "address__state", "preferred_carriers__carrier")

    # list_display = ("first_name", "email", "phone", "zip_code", "get_address", "reference", "easy_access_to_loading", "parking_available")
    list_display = ("first_name", "email", "phone", "reference", "easy_access_to_loading", "parking_available")

    fieldsets = [
        (
            None,
            {
                # "fields": [("first_name", "email"), ("phone", "zip_code"), "get_address"],
                "fields": [("first_name", "email"), ("phone")],

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



# admin.site.register(Individual)


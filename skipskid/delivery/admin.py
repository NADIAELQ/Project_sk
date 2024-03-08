from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Delivery, DeliveryAddress, DeliveryPhoto

# Register your models here.

class DeliveryPhotoInline(admin.TabularInline):
    model = DeliveryPhoto

@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    icon = "location_on"

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    search_fields = ('number',)
    list_filter = ('status', 'pick_up_address__shipper', 'hazmat', 'date_created', 'pick_up_address__postcode')
    list_display = ("pick_up_address", "drop_off_address", "pick_up_date", "drop_off_date", "reference", "rate", "status", "date_created")
    icon = "Package 2"
    exclude = ('date_created', 'dimensions')

    fieldsets = (
        (_("Delivery details"), {
            "fields": (
                "pick_up_address", "drop_off_address", "pick_up_date", "drop_off_date",
                "status", "rate", "weight", "recommended_vehicles", "hazmat", "description"
            )
        }),
        (_("Pick up informations"), {
            "fields": (
                "pick_up_instructions",
            )
        }),
        (_("Drop off informations"), {
            "fields": (
                "drop_off_instructions",
            )
        }),
    )

    @admin.display(description=_("Shipper"))
    def get_shipper(self, instance, **kwargs):
        return instance.pick_up_address.shipper

    @admin.display(description=_("P/U Date"))
    def get_pick_up_date(self, instance, **kwargs):
        return instance.pick_up_date.strftime("%x")

    @admin.display(description=_("P/U Time"))
    def get_pick_up_time(self, instance, **kwargs):
        return instance.pick_up_date.strftime("%H:%M")

    @admin.display(description=_("Phone at pick up"))
    def get_pick_up_phone_number(self, instance, **kwargs):
        return instance.drop_off_address.phone_number

    @admin.display(description=_("Contact person at pick up"))
    def get_pick_up_contact_person(self, instance, **kwargs):
        return instance.pick_up_address.contact_person

    @admin.display(description=_("D/OFF Date"))
    def get_drop_off_date(self, instance, **kwargs):
        return instance.drop_off_date.strftime("%x")

    @admin.display(description=_("D/OFF Time"))
    def get_drop_off_time(self, instance, **kwargs):
        return instance.drop_off_date.strftime("%H:%M")

    @admin.display(description=_("Phone at dropp off"))
    def get_drop_off_phone_number(self, instance, **kwargs):
        return instance.drop_off_address.phone_number

    @admin.display(description=_("Contact person at drop off"))
    def get_drop_off_contact_person(self, instance, **kwargs):
        return instance.drop_off_address.contact_person

    # fieldsets = (
    #     (_("Delivery details"), {
    #         "fields": (
    #             "pick_up_address", "drop_off_address", "pick_up_date", "drop_off_date",
    #             "status", "rate", "dimensions", "weight", "recommended_vehicles", "hazmat", "description"
    #         )
    #     }),
    #     (_("Pick up informations"), {
    #         "fields": (
    #             "pick_up_instructions",
    #         )
    #     }),
    #     (_("Drop off informations"), {
    #         "fields": (
    #             "drop_off_instructions",
    #         )
    #     }),
    # )

    # Allow superusers to add, change, and delete instances
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    inlines = [DeliveryPhotoInline]

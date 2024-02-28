from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Delivery, DeliveryAddress


# Register your models here.


@admin.register(DeliveryAddress)
class DeliveryAdmin(admin.ModelAdmin):
    list_filter = ('name',)

    icon = "location_on"


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):

    search_fields = ('number',)
    list_filter = ('status', 'pick_up_address__shipper', 'hazmat', 'date_created', 'pick_up_address__postcode')
    list_display = ("get_shipper", "pick_up_address", "drop_off_address", "get_pick_up_date", "get_pick_up_time", "get_drop_off_date", "get_drop_off_time", "reference", "rate", "status")

    icon = "Package 2"

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


    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


    fieldsets = (
        (_("Delivery details"), {"fields": (
            ("get_shipper", "date_created"),
            ("status", "rate"),
            ("dimensions", "weight"),
            ("recommended_vehicles", "hazmat"),
            "description"
        )}),
        (_("Pick up informations"), {"fields": (
            ("pick_up_date", "pick_up_address"),
            ("get_pick_up_contact_person", "get_pick_up_phone_number"),
            "pick_up_instructions"
        )}),

        (_("Drop off informations"), {"fields": (
            ("drop_off_date", "drop_off_address"),
            ('get_drop_off_contact_person', 'get_drop_off_phone_number'),
            "drop_off_instructions"
        )}),
    )

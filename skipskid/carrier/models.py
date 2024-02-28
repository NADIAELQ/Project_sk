from django.db import models
from django.contrib import admin
from django.core.validators import EMPTY_VALUES, MinValueValidator
from django.utils.translation import gettext_lazy as _

from address.models import AbstractAddress
from equipment.models import VehicleType, EquipmentType


# Create your models here.


class Carrier(models.Model):

    name = models.CharField(_("Carrier name"), max_length=100, db_index=True)
    about = models.CharField(_("About the Company"), max_length=200, null=True, blank=True)
    contact_person = models.CharField(_("Contact person"), max_length=100, db_index=True)
    email = models.EmailField(_("Business email"), null=True, blank=True)
    phone_number = models.CharField(_("Business Phone"), max_length=30, null=True, blank=True)
    website = models.URLField(_("Website"), null=True, blank=True)
    pounds_plus = models.BooleanField(_("Can load/unload 150+ pounds"), choices=((False, _("No")), (True, _("Yes"))), default=False)
    miles_plus = models.BooleanField(_("Can travel over 150 miles"), choices=((False, _("No")), (True, _("Yes"))), default=False)
    sequence = models.PositiveSmallIntegerField(unique=True, editable=False, db_index=True)

    def save(self, **kwargs):
        if self.sequence in EMPTY_VALUES:
            self.sequence = self._get_next_sequence()
        return super().save(**kwargs)

    def _get_next_sequence(self):
        last_sequence = self.__class__.objects.aggregate(models.Max('sequence'))['sequence__max'] or 1000
        return last_sequence + 1

    def __str__(self):
        return self.name

    @property
    @admin.display(description=_("Reference"))
    def reference(self):
        return "C%s" % (self.sequence or self._get_next_sequence())

    @property
    @admin.display(description=_("Types of Vehicles"))
    def types_of_vehicles(self):
        return ", ".join([v.type.name for v in self.vehicles.all()])

    @property
    @admin.display(description=_("Number of available vehicles"))
    def num_vehicles(self):
        return self.vehicles.all().count()

    class Meta:
        default_permissions = ["view", "change", "delete"]
        verbose_name = _("Carrier")
        verbose_name_plural = _("Carriers")



class CarrierAddress(AbstractAddress):

    carrier = models.OneToOneField(Carrier, on_delete=models.CASCADE, null=True, blank=True, related_name="address", verbose_name=_("Carrier"))

    class Meta:
        default_permissions = ["view", "change", "delete"]
        verbose_name = _("Carrier\'s address")


class CarrierVehicle(models.Model):

    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE, related_name="vehicles", verbose_name=_("Carrier"))
    type = models.ForeignKey(VehicleType, on_delete=models.CASCADE, verbose_name=_("Type of Vehicle"))
    number = models.PositiveSmallIntegerField(_("Number"), default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return "%s (%s)" % (self.type, self.number)

    class Meta:
        unique_together = ["carrier", "type"]
        default_permissions = ["view", "change", "delete"]
        verbose_name = _("Carrier\'s vehicle")
        verbose_name_plural = _("Carrier\'s vehicles")


class CarrierEquipment(models.Model):

    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE, related_name="equipments", verbose_name=_("Carrier"))
    type = models.ForeignKey(EquipmentType, on_delete=models.CASCADE, verbose_name=_("Type of equipment"))
    number = models.PositiveSmallIntegerField(_("Number"), default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return self.type.name

    class Meta:
        unique_together = ["carrier", "type"]
        default_permissions = ["view", "change", "delete"]
        verbose_name = _("Carrier\'s equipment")
        verbose_name_plural = _("Carrier\'s equipments")


class Certification(models.Model):

    name = models.CharField(_("Name"), max_length=200, unique=True)
    description = models.TextField(_("Description"), blank=True, null=True)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Certification")
        verbose_name_plural = _("Certifications")


class CarrierCertification(models.Model):

    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE, related_name="certifications", verbose_name=_("Carrier"))
    certification = models.ForeignKey(Certification, on_delete=models.CASCADE, verbose_name=_("Certification"))

    class Meta:
        unique_together = ['carrier', 'certification']
        verbose_name = _("Carrier certification")
        verbose_name = _("Carrier certifications")

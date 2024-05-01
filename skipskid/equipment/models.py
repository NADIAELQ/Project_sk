from django.db import models
from django.utils.translation import gettext_lazy as _

class VehicleType(models.Model):

    name = models.CharField(_("Vehicle type"), max_length=200, unique=True)

    def __str__(self):
        return self.name


class EquipmentType(models.Model):

    name = models.CharField(_("Equipment name"), max_length=200, unique=True)

    def __str__(self):
        return self.name

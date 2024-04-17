from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import UserManager
from django.db import models
# from .manager import CarrierUserManager
from django.contrib import admin
from django.core.validators import EMPTY_VALUES, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.contrib.auth.models import Group, Permission

from address.models import AbstractAddress
from equipment.models import VehicleType, EquipmentType


# Create your models here.


class Carrier(AbstractUser):

    name = models.CharField(_("Carrier name"), max_length=100, db_index=True)
    about = models.CharField(_("About the Company"), max_length=200, null=True, blank=True)
    contact_person = models.CharField(_("Contact person"), max_length=100, db_index=True)
    email = models.EmailField(_("Business email"), null=True, blank=True, unique=True)
    phone_number = models.CharField(_("Business Phone"), max_length=30, null=True, blank=True)
    website = models.URLField(_("Website"), null=True, blank=True)
    pounds_plus = models.BooleanField(_("Can load/unload 150+ pounds"), choices=((False, _("No")), (True, _("Yes"))), default=False)
    miles_plus = models.BooleanField(_("Can travel over 150 miles"), choices=((False, _("No")), (True, _("Yes"))), default=False)
    sequence = models.PositiveSmallIntegerField(unique=True, editable=False, db_index=True)
    password = models.CharField(_("Password"), max_length=128, null=True, blank=True, default='')
    password_reset_token = models.CharField(max_length=100, blank=True, null=True, default='')

    username=None
    
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # last_login = models.DateTimeField(_('last login'), default=timezone.now, column_name='last_login_date')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]

    def save(self, **kwargs):
        if self.sequence in EMPTY_VALUES:
            self.sequence = self._get_next_sequence()
        return super().save(**kwargs)

    def _get_next_sequence(self):
        last_sequence = self.__class__.objects.aggregate(models.Max('sequence'))['sequence__max'] or 1000
        return last_sequence + 1

    def __str__(self):
        return self.email

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
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    class Meta:
        default_permissions = ["view", "change", "delete"]
        verbose_name = _("Carrier")
        verbose_name_plural = _("Carriers")

    groups = models.ManyToManyField(Group, related_name='carrier_groups', verbose_name=_("Groups"), blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='carrier_permissions', verbose_name=_("User permissions"), blank=True)

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

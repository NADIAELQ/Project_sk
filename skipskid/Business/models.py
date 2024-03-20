from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager

from django.db import models
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
from carrier.models import Carrier

class Business(AbstractUser):
    business_name = models.CharField(_("Business Name"), max_length=255, db_index=True)
    # type_of_industry = models.CharField(_("Type of Industry"), max_length=255, null=True, blank=True)
    contact_person = models.CharField(_("Contact Person"), max_length=255, db_index=True)
    business_email = models.EmailField(_("Business Email"), max_length=255, db_index=True)
    business_phone = models.CharField(_("Business Phone"), max_length=30, null=True, blank=True)
    website = models.URLField(_("Website"), blank=True, null=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    sequence = models.PositiveSmallIntegerField(unique=True, editable=False, db_index=True)

    password = models.CharField(_("Password"), max_length=128, null=True, blank=True, default='')
    password_reset_token = models.CharField(max_length=100, blank=True, null=True, default='')

    username=None
    
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'business_email'
    REQUIRED_FIELDS=[]


    def save(self, **kwargs):
        if self.sequence in EMPTY_VALUES:
            self.sequence = self._get_next_sequence()
        return super().save(**kwargs)
 
    def _get_next_sequence(self):
        last_sequence = self.__class__.objects.aggregate(models.Max('sequence'))['sequence__max'] or 1000
        return last_sequence + 1

    def __str__(self):
        return self.business_name

    @property
    @admin.display(description=_("Reference"))
    def reference(self):
        return "B%s" % (self.sequence or self._get_next_sequence())
    
    # Checkboxes
    has_loading_dock = models.BooleanField(_("Loading Dock"), choices=((False, _("No")), (True, _("Yes"))), default=False)
    has_forklift = models.BooleanField(_("Forklift"), choices=((False, _("No")), (True, _("Yes"))), default=False)
    has_ramp = models.BooleanField(_("Ramp"), choices=((False, _("No")), (True, _("Yes"))), default=False)

    # # Unique identifying Account Number
    # account_number = models.CharField(_("Account Number"), max_length=255, unique=True)

        
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='business_groups', 
        related_query_name="business",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='business_user_permissions',
        related_query_name="business",
    )

    class Meta:
        verbose_name = _("Business (Shipper)")
        verbose_name_plural = _("Businesses (Shippers)")



class BusinessAddress (AbstractAddress):

    business = models.OneToOneField(Business, on_delete=models.CASCADE, null=True, blank=True, related_name="address", verbose_name=_("Business"))

    class Meta:
        default_permissions = ["view", "change", "delete"]
        verbose_name = _("Business's address")


class TypeOfIndustry(models.Model):

    name = models.CharField(_("Name"), max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Type of industry")
        # verbose_name_plural = _("Types of")


class BusinessTypeOfIndustry(models.Model):

    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="Type_of_industries", verbose_name=_("Business"))
    TypeOfIndustry = models.ForeignKey(TypeOfIndustry, on_delete=models.CASCADE, verbose_name=_("Type of industry"))

    class Meta:
        unique_together = ['business', 'TypeOfIndustry']
        verbose_name = _("Business type of industry")
        # verbose_name_plural = _("Business type of industry")

        
class ShipperEquipment(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='equipments')
    type = models.CharField(max_length=100)
    number = models.IntegerField()

    def __str__(self):
        return f"{self.business.business_name} - {self.type}"

    class Meta:
        verbose_name = "Shipper Equipment"
        verbose_name_plural = "Shipper Equipments"


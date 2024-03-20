from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
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


class Individual(AbstractUser):
    first_name = models.CharField(_("First Name"), max_length=255)
    # a revoirr
    # home_zip_code = models.CharField(_("Home Zip Code"), max_length=10)
    email = models.EmailField(_("Email"))
    phone = models.CharField(_("Phone"), max_length=30)
    parking_available = models.BooleanField(_("Parking available"), max_length=5, choices=(("no", _("No")), ("yes", _("Yes"))), default="no")
    easy_access_to_loading = models.BooleanField(_("Easy access to loading"),  max_length=5, choices=(("no", _("No")), ("yes", _("Yes"))), default="no")
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

    @property
    def zip_code(self):
        if self.address :
            return self.address.postcode
        return None

    def save(self, **kwargs):
        if self.sequence in EMPTY_VALUES:
            self.sequence = self._get_next_sequence()
        return super().save(**kwargs)
 
    def _get_next_sequence(self):
        last_sequence = self.__class__.objects.aggregate(models.Max('sequence'))['sequence__max'] or 1000
        return last_sequence + 1

    def __str__(self):
        return self.first_name

    @property
    @admin.display(description=_("Reference"))
    def reference(self):
        return "V%s" % (self.sequence or self._get_next_sequence())
    
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='individual_groups',  
        related_query_name="individual",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='individual_user_permissions',
        related_query_name="individual",
    )

    class Meta:
        verbose_name = _("Individual Profile")
        verbose_name_plural = _("Individual Profiles")


class IndividualAddress (AbstractAddress):

    individual = models.OneToOneField(Individual, on_delete=models.CASCADE, null=True, blank=True, related_name="address", verbose_name=_("Individual"))

    class Meta:
        default_permissions = ["view", "change", "delete"]
        verbose_name = _("Individual's address")


class IndividualPreferredCarrier(models.Model):
    individual = models.ForeignKey(Individual, on_delete=models.CASCADE, related_name="preferred_carriers", verbose_name=_("Individual"))
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE, verbose_name=_("Preferred Carrier"))

    def __str__(self):
        return f"PreferredCarrier for {self.individual.first_name}"

    class Meta:
        verbose_name = _("Preferred Carrier")
        verbose_name_plural = _("Preferred Carriers")


class IndividualDelivery(models.Model):
    individual = models.ForeignKey(Individual, on_delete=models.CASCADE, related_name="deliveries", verbose_name=_("Individual"))
    origin = models.CharField(_("Origin"), max_length=255)
    destination = models.CharField(_("Destination"), max_length=255)
    status = models.CharField(_("Status"), max_length=100)
    pickup_date = models.DateTimeField(_("Pick Up Date"))
    delivery_date = models.DateTimeField(_("Delivery Date"))
    assigned_carrier = models.ForeignKey(Carrier, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Assigned Carrier"))
    offers = models.IntegerField(_("Offers"), default=0)


    def __str__(self):
        return f"Delivery for {self.individual.first_name} from {self.origin} to {self.destination}"

    class Meta:
        verbose_name = _("Individual Delivery")
        verbose_name_plural = _("Individual Deliveries")
        

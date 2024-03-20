from django.db import models
from django.contrib import admin
from django.core.validators import EMPTY_VALUES, MinValueValidator
from django.utils.translation import gettext_lazy as _
from shipper.models import Shipper

from address.models import AbstractAddress
from carrier.models import Carrier


class BusinessShipper(Shipper):
    class Meta:
        verbose_name = "Business Shipper"
        verbose_name_plural = "Business Shippers"

class IndividualShipper(Shipper):
    class Meta:
        verbose_name = "Individual Shipper"
        verbose_name_plural = "Individual Shippers"


class Business(models.Model):
    business_name = models.CharField(_("Business Name"), max_length=255, db_index=True)
    # type_of_industry = models.CharField(_("Type of Industry"), max_length=255, null=True, blank=True)
    contact_person = models.CharField(_("Contact Person"), max_length=255, db_index=True)
    business_email = models.EmailField(_("Business Email"), max_length=255, db_index=True)
    business_phone = models.CharField(_("Business Phone"), max_length=30, null=True, blank=True)
    website = models.URLField(_("Website"), blank=True, null=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    sequence = models.PositiveSmallIntegerField(unique=True, editable=False, db_index=True)
    
    shipper_type = models.ForeignKey(BusinessShipper, on_delete=models.CASCADE)

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



class Individual(Shipper):
    first_name = models.CharField(_("First Name"), max_length=255)
    # a revoirr
    # home_zip_code = models.CharField(_("Home Zip Code"), max_length=10)
    email = models.EmailField(_("Email"))
    phone = models.CharField(_("Phone"), max_length=30)
    parking_available = models.BooleanField(_("Parking available"), max_length=5, choices=(("no", _("No")), ("yes", _("Yes"))), default="no")
    easy_access_to_loading = models.BooleanField(_("Easy access to loading"),  max_length=5, choices=(("no", _("No")), ("yes", _("Yes"))), default="no")
    sequence = models.PositiveSmallIntegerField(unique=True, editable=False, db_index=True)

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
        
class ShipperEquipment(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='equipments')
    type = models.CharField(max_length=100)
    number = models.IntegerField()

    def __str__(self):
        return f"{self.business.business_name} - {self.type}"

    class Meta:
        verbose_name = "Shipper Equipment"
        verbose_name_plural = "Shipper Equipments"


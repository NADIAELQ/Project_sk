from django.db import models
from django.contrib import admin
from django.core.validators import EMPTY_VALUES, MinValueValidator
from django.core.mail import send_mail
from django.utils import timezone
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.contrib.auth.models import User
from address.models import AbstractAddress
from carrier.models import Carrier

class TypeOfIndustry(models.Model):

	name = models.CharField("Name", max_length=200, unique=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Type of industry"
		verbose_name_plural = "types of industries"


class ShipperUser(User):

	class Meta:
		proxy = True
		verbose_name = "Shipper"
		verbose_name_plural = "Shippers"


class Shipper(models.Model):

	user = models.OneToOneField(ShipperUser, on_delete=models.CASCADE, related_name="shipper_profile")

	BUSINESS, INDIVIDUAL = "B", "V"
	SHIPPER_TYPES = (
		(BUSINESS, "Business"),
		(INDIVIDUAL, "Individual")
	)
	type = models.CharField("Type", max_length=20, choices=SHIPPER_TYPES)

	name = models.CharField("Name", max_length=255, db_index=True)
	email_address = models.EmailField("Business Email", max_length=255, db_index=True)
	phone_number = models.CharField("Business Phone", max_length=30)

	sequence = models.PositiveSmallIntegerField(unique=True, editable=False, db_index=True)
	date_created = models.DateTimeField("Date created", auto_now_add=True)

	def _get_next_sequence(self, type):
		last_sequence = self.__class__.objects.filter(type=type).aggregate(models.Max('sequence'))['sequence__max'] or 1000
		return last_sequence + 1

	def save(self, **kwargs):
		if self.sequence in EMPTY_VALUES:
			self.sequence = self._get_next_sequence(self.type)
		return super().save(**kwargs)

	def __str__(self):
		return self.name

	@property
	@admin.display(description="Reference")
	def reference(self):
		if self.pk:
			return "%s%s" % (self.type, self.sequence)
		return "%s%s" % (self.type, self._get_next_sequence())

	class Meta:
		verbose_name = "Shipper"
		verbose_name_plural = "Shippers"


class Individual(models.Model):

	shipper = models.OneToOneField(Shipper, on_delete=models.CASCADE, verbose_name="Shipper")
	parking_available = models.BooleanField("Parking available", choices=((True, "Yes"), (False,"No")))
	easy_access_to_loading = models.BooleanField("Easy access to loading", choices=((True, "Yes"), (False,"No")))

	@property
	@admin.display(description="Reference")
	def reference(self):
		return self.shipper.reference

	@property
	@admin.display(description="Full name")
	def full_name(self):
		return self.shipper.name

	@property
	@admin.display(description="Email address")
	def email_address(self):
		return self.shipper.email_address

	@property
	@admin.display(description="Phone number")
	def phone_number(self):
		return self.shipper.phone_number

	@property
	def zip_code(self):
		if self.address:
		    return self.address.postcode
		return None

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Individual"
		verbose_name_plural = "Individuals"

	def __str__(self):
		return str(self.shipper.__str__)

	class Meta:
		verbose_name = "Individual"
		verbose_name_plural = "Individuals"


class Business(models.Model):

	shipper = models.OneToOneField(Shipper, on_delete=models.CASCADE)
	type_of_industry = models.ForeignKey(TypeOfIndustry, on_delete=models.CASCADE, verbose_name="Type of industry")
	contact_person = models.CharField("Contact Person", max_length=255, db_index=True)
	website = models.URLField("Website", blank=True, null=True)
	image = models.ImageField(upload_to='images/', null=True, blank=True)

	has_loading_dock = models.BooleanField("Loading Dock", choices=((True, "Yes"), (False,"No")))
	has_forklift = models.BooleanField("Forklift", choices=((True, "Yes"), (False,"No")))
	has_ramp = models.BooleanField("Ramp", choices=((True, "Yes"), (False,"No")))

	sequence = models.PositiveSmallIntegerField(unique=True, editable=False, db_index=True)
	date_created = models.DateTimeField("Date created", auto_now_add=True)

	def _get_next_sequence(self):
		last_sequence = self.__class__.objects.aggregate(models.Max('sequence'))['sequence__max'] or 1000
		return last_sequence + 1

	def save(self, **kwargs):
		if self.sequence in EMPTY_VALUES:
			self.sequence = self._get_next_sequence()
		return super().save(**kwargs)

	@property
	@admin.display(description="Reference")
	def reference(self):
		return self.shipper.reference

	@property
	@admin.display(description="Business Name")
	def business_name(self):
		return self.shipper.name

	@property
	@admin.display(description="Business Email")
	def business_email(self):
		return self.shipper.email_address

	@property
	@admin.display(description="Business Phone")
	def business_phone(self):
		return self.shipper.phone_number

	def __str__(self):
		return str(self.shipper.__str__)

	class Meta:
		verbose_name = "Business"
		verbose_name_plural = "Businesses"


class BusinessAddress(AbstractAddress):

	business = models.OneToOneField(Business, on_delete=models.CASCADE, related_name="address", verbose_name="Business")

	class Meta:
		verbose_name = "Business address"
		verbose_name = "Business addresses"


class IndividualAddress(AbstractAddress):

    individual = models.OneToOneField(Individual, on_delete=models.CASCADE, related_name="address", verbose_name="Individual")

    class Meta:
        verbose_name = "Individual Zip Code"
        verbose_name_plural = "Individual Zip Codes"

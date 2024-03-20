# from django.db import models
# from django.contrib import admin
# from django.core.validators import EMPTY_VALUES, MinValueValidator
# from django.utils.translation import gettext_lazy as _

# from SkipSkid.skipskid.address.models import AbstractAddress
# from carrier.models import CarrierAddress



# # Create your models here.


# class Shipper(models.Model):

#     business_name = models.CharField(_("Business Name"), max_length=255, db_index=True)
# #     type_of_industry = models.CharField(_("Type of Industry"), max_length=255, null=True, blank=True)
# #     contact_person = models.CharField(_("Contact Person"), max_length=255, db_index=True)
# #     business_email = models.EmailField(_("Business Email"), max_length=255, db_index=True)
# #     business_phone = models.CharField(_("Business Phone"), max_length=30, null=True, blank=True)
# #     website = models.URLField(_("Website"), blank=True, null=True)
# #     sequence = models.PositiveSmallIntegerField(unique=True, editable=False, db_index=True)

# #     def save(self, **kwargs):
# #         if self.sequence in EMPTY_VALUES:
# #             self.sequence = self._get_next_sequence()
# #         return super().save(**kwargs)

# #     def _get_next_sequence(self):
# #         last_sequence = self.__class__.objects.aggregate(models.Max('sequence'))['sequence__max'] or 1000
# #         return last_sequence + 1

# #     def __str__(self):
# #         return self.business_name
    
# #     @property
# #     @admin.display(description=_("Reference"))
# #     def reference(self):
# #         return "B%s" % (self.sequence or self._get_next_sequence())
    
# #      # Checkboxes
# #     has_loading_dock = models.BooleanField(_("Loading Dock"), choices=((False, _("No")), (True, _("Yes"))), default=False)
# #     has_forklift = models.BooleanField(_("Forklift"), choices=((False, _("No")), (True, _("Yes"))), default=False)
# #     has_ramp = models.BooleanField(_("Ramp"), choices=((False, _("No")), (True, _("Yes"))), default=False)

   
# #     class Meta:
# #         verbose_name = _("Business (Shipper)")
# #         verbose_name_plural = _("Businesses (Shippers)")


# # class ShipperAddress (AbstractAddress):

# #     business = models.OneToOneField(Shipper, on_delete=models.CASCADE, null=True, blank=True, related_name="address", verbose_name=_("Business"))

# #     class Meta:
# #         default_permissions = ["view", "change", "delete"]
# #         verbose_name = _("Business's address")

# # class TypeOfIndustry(models.Model):

# #     name = models.CharField(_("Name"), max_length=200, unique=True)

# #     def __str__(self):
# #         return self.name

# #     class Meta:
# #         verbose_name = _("Type of industry")
# #         # verbose_name_plural = _("Types of")

# # class BusinessTypeOfIndustry(models.Model):

# #     business = models.ForeignKey(Shipper, on_delete=models.CASCADE, related_name="Type_of_industries", verbose_name=_("Business"))
# #     TypeOfIndustry = models.ForeignKey(TypeOfIndustry, on_delete=models.CASCADE, verbose_name=_("Type of industry"))

# #     class Meta:
# #         unique_together = ['business', 'TypeOfIndustry']
# #         verbose_name = _("Business type of industry")
# #         # verbose_name_plural = _("Business type of industry")

from django.db import models


# Create your models here.


class Shipper(models.Model):

    name = models.CharField(max_length=200)

    def _str_(self):
        return self.name
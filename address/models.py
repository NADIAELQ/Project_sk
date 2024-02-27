from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

import re
import zlib


class AbstractAddress(models.Model):

    POSTCODE_REGEX = r"^[0-9]{5}(-[0-9]{4}|-[0-9]{6})?$"

    line1 = models.CharField(_("First line of address"), max_length=255)
    line2 = models.CharField(_("Second line of address"), max_length=255, null=True, blank=True)
    city = models.CharField(_("City"), max_length=255, blank=True)
    state = models.CharField(_("State"), max_length=255, null=True, blank=True)
    postcode = models.CharField(_("Zip Code"), max_length=64, null=True, blank=True, db_index=True)

    # A field only used for searching addresses - this contains all the
    # `search_fields`.  This is effectively a poor man's Solr text field.
    search_text = models.TextField(_("Search text - used only for searching addresses"), editable=False)
    search_fields = ["line1", "line2", "city", "state", "postcode"]

    # Fields, used for `summary` property definition and hash generation.
    base_fields = ["line1", "line2", "city", "state", "postcode"]
    hash_fields = ["line1", "line2", "city", "state", "postcode"]

    def __str__(self):
        return self.summary

    class Meta:
        abstract = True
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def save(self, *args, **kwargs):
        self._update_search_text()
        super().save(*args, **kwargs)

    def clean(self):
        # Strip all whitespace
        for field in ["line1", "line2", "city", "state", "postcode"]:
            if self.__dict__[field]:
                self.__dict__[field] = self.__dict__[field].strip()

        # Ensure postcodes are valid for country
        self.ensure_postcode_is_valid_for_country()

    def ensure_postcode_is_valid_for_country(self):

        if self.postcode:
            # Ensure postcodes are always uppercase
            postcode = self.postcode.upper().replace(" ", "")

            if not re.match(self.POSTCODE_REGEX, postcode):
                msg = _("The postcode '%(postcode)s' is not valid") % {
                    "postcode": self.postcode,
                }
                raise ValidationError({"postcode": [msg]})

    def _update_search_text(self):
        self.search_text = self.join_fields(self.search_fields, separator=" ")

    # Properties

    @property
    def summary(self):
        #Returns a single string summary of the address, separating fields using commas.
        #ex. Address: 6314 Walls drive, New England, MA 10111
        return ", ".join(self.active_address_fields())

    # Helpers

    def generate_hash(self):
        """
        Returns a hash of the address, based on standard set of fields, listed
        out in `hash_fields` property.
        """
        field_values = self.get_address_field_values(self.hash_fields)
        # Python 2 and 3 generates CRC checksum in different ranges, so
        # in order to generate platform-independent value we apply
        # `& 0xffffffff` expression.
        return zlib.crc32(", ".join(field_values).upper().encode("UTF8")) & 0xFFFFFFFF

    def join_fields(self, fields, separator=", "):
        """
        Join a sequence of fields using the specified separator
        """
        field_values = self.get_field_values(fields)
        return separator.join(filter(bool, field_values))

    def populate_alternative_model(self, address_model):
        """
        For populating an address model using the matching fields
        from this one.

        This is used to convert a user address to a shipping address
        as part of the checkout process.
        """
        destination_field_names = [field.name for field in address_model._meta.fields]
        for field_name in [field.name for field in self._meta.fields]:
            if field_name in destination_field_names and field_name != "id":
                setattr(address_model, field_name, getattr(self, field_name))

    def active_address_fields(self):
        """
        Returns the non-empty components of the address, but merging the
        title, first_name and last_name into a single line. It uses fields
        listed out in `base_fields` property.
        """
        return self.get_address_field_values(self.base_fields)

    def get_address_field_values(self, fields):
        """
        Returns set of field values within the salutation and country.
        """
        field_values = [f.strip() for f in self.get_field_values(fields) if f]
        return field_values

    def get_field_values(self, fields):
        field_values = []
        for field in fields:
            value = getattr(self, field)
            field_values.append(value)
        return field_values

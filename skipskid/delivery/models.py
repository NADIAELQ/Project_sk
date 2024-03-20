from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from address.models import AbstractAddress
from equipment.models import VehicleType
from Business.models import Business
from Individual.models import Individual
from django.shortcuts import get_object_or_404

from . import exceptions
from .managers import ActiveDeliveryManager
from .signals import delivery_status_changed


# Create your models here.
Shipper=[
    ('Individual','Individual'),
    ('Business','Business')
]

class Shipper(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)

    user_type = models.CharField(max_length=32, choices=Shipper)

class DeliveryAddress(AbstractAddress):

    #line1, line2, city, state, postcode
    name = models.CharField(_("Name/Business"), max_length=100, db_index=True)
    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE, related_name="addresses", verbose_name=_("Shipper"))

    PICK_UP, DROP_OFF = "Pick up", "Drop off"
    TYPE_CHOICES = (
        (PICK_UP, _("Pick up")),
        (DROP_OFF, _("Drop off"))
    )
    type = models.CharField(_("Type"), max_length=100, choices=TYPE_CHOICES)

    contact_person = models.CharField(_("Contact person"), max_length=100, db_index=True)
    phone_number = models.CharField(_("Phone number"), max_length=30, null=True, blank=True)

    def save(self, *args, **kwargs):
        Shipper = get_object_or_404(Shipper, id=self.Shipper.id)
        if Shipper.user_type != 'Shipper':
            raise ValueError('selected user must be Shipper')
        super().save(*args, **kwargs)


    class Meta:
        default_permissions = ['view']
        verbose_name = _("Delivery address")
        verbose_name_plural = _("Delivery addresses")


class Delivery(models.Model):

    rate = models.DecimalField(_("Rate"), decimal_places=2, max_digits=11)
    weight = models.DecimalField(_("Weight (lbs)"), decimal_places=2, max_digits=11)
    width = models.DecimalField(_("Width"), decimal_places=2, max_digits=11)
    height = models.DecimalField(_("Height"), decimal_places=2, max_digits=11)
    depth = models.DecimalField(_("Depth"), decimal_places=2, max_digits=11)
    description = models.TextField(_("Description of Delivery"))

    recommended_vehicles = models.ManyToManyField(VehicleType, verbose_name=_("Recommended Vehicles"))
    hazmat = models.BooleanField(_("Hazmat"), choices=((False, _("No")), (True, _("Yes"))))

    '''
    Business Name: Walton Industries
    Pick Up Address: 29 Palms Road, Fresno, CA 93650
    Contact Person at Pick Up: Joe Mann
    Phone at Pick Up: 502-214-2145
    '''
    pick_up_address = models.ForeignKey(DeliveryAddress, on_delete=models.PROTECT, related_name="pick_up_deliveries", verbose_name=_("Pick Up Address"))
    pick_up_date = models.DateTimeField(_("Pick up date"))
    pick_up_instructions = models.TextField(_("Pick up instructions"), null=True, blank=True)

    '''
    Deliver to (Business or Name): Jay Rod Plumbing
    Delivery Address: 50 W Allan Court, Fresno, CA 93650
    Contact Person at Drop Off: Adam Freeman
    Phone at Drop Off: 513-251-1234
    '''
    drop_off_address = models.ForeignKey(DeliveryAddress, on_delete=models.PROTECT, related_name="drop_off_deliveries", verbose_name=_("Drop off Address"))
    drop_off_date = models.DateTimeField(_("Drop off Date"))
    drop_off_instructions = models.TextField(_("Drop off instructions"), null=True, blank=True)

    number = models.CharField(_("Delivery ID"), max_length=100, db_index=True, unique=True)
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)

    ACTIVE = "Active"
    ASSIGNED = "Assigned"
    ACCEPTED = "Accepted"
    GAINED = "Gained"
    IN_TRANSIT = "In transit"
    COMPLETE = 'Complete'
    DROPPED = 'Dropped'
    CANCELLED = 'Cancelled'

    STATUS_CHOICES = (
        (ACTIVE, _("Active")),
        (ASSIGNED, _("Assigned to Carrier")),
        (ACCEPTED, _("Accepted by Carrier")),
        (GAINED, _("Gained from an offer")),
        (IN_TRANSIT, _("In transit")),
        (COMPLETE, _("Complete")),
        (DROPPED, _("Dropped")),
        (CANCELLED, _("Cancelled")),
    )
    status = models.CharField(_("Status"), max_length=100, default=ACTIVE, choices=STATUS_CHOICES)

    uneditable_statuses = (COMPLETE, )

    pipeline = {
        ACTIVE: (ASSIGNED, CANCELLED),
        ASSIGNED: (ACCEPTED, ),
        ACCEPTED: (IN_TRANSIT, COMPLETE),
        GAINED: (IN_TRANSIT, COMPLETE),
        IN_TRANSIT: (COMPLETE, ),
        COMPLETE: (),
        DROPPED: (CANCELLED, ACTIVE, ASSIGNED),
        CANCELLED: (ACTIVE, ),
    }

    active = ActiveDeliveryManager()

    @classmethod
    def all_statuses(cls):
        return list(cls.pipeline.keys())

    def available_statuses(self):
        return self.pipeline.get(self.status, ())

    def set_status(self, new_status):

        if new_status == self.status:
            return

        old_status = self.status

        if new_status not in self.available_statuses():
            raise exceptions.InvalidDeliveryStatus(
                _("'%(new_status)s' is not a valid status for delivery '%(number)s'. (current status: '%(status)s')")
                % {"new_status": new_status, "number": self.number, "status": self.status}
            )

        self.status = new_status
        self.save()

        # Send signal for handling status changed
        delivery_status_changed.send(sender=self, delivery=self, old_status=old_status, new_status=new_status)

        self._create_delivery_status_change(old_status, new_status)

    set_status.alters_data = True

    def _create_delivery_status_change(self, old_status, new_status):
        # Not setting the status on the delivery as that should be handled before
        self.status_changes.create(old_status=old_status, new_status=new_status)

    class Meta:
        ordering = ["-date_created"]
        default_permissions = ['view', 'change', 'delete']
        verbose_name = _("Delivery")
        verbose_name_plural = _("Deliveries")

    def __str__(self):
        return self.reference

    @property
    @admin.display(description=_("Dimenstions"))
    def dimensions(self):
        return "%s”X%s”X%s" % (self.width, self.height, self.depth)

    @property
    @admin.display(description=_("Delivery ID"))
    def reference(self):
        return "D%s" % self.number


class DeliveryPhoto(models.Model):
    delivery = models.ForeignKey(
        Delivery, on_delete=models.CASCADE, related_name="photos"
    )
    photo = models.ImageField()




class DeliveryStatusChange(models.Model):

    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name="status_changes", verbose_name=_("Delivery"))
    old_status = models.CharField(_("Old Status"), max_length=100, null=True, blank=True)
    new_status = models.CharField(_("New Status"), max_length=100, null=True, blank=True)
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True, db_index=True)

    class Meta:
        default_permissions = ['view']
        verbose_name = _("Delivery Status Change")
        verbose_name_plural = _("Delivery Status Changes")
        ordering = ["-date_created"]

    def __str__(self):
        return _(
            "%(delivery)s has changed status from %(old_status)s to %(new_status)s") % {
                "delivery": self.delivery,
                "old_status": self.old_status,
                "new_status": self.new_status,
            }

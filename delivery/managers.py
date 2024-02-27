from django.db import models


class ActiveDeliveryManager(models.Manager):

    """For searching/creating ACTIVE deliveries only."""

    status_filter = "Active"

    def get_queryset(self):
        return super().get_queryset().filter(status=self.status_filter)

    def get_or_create(self, **kwargs):
        return self.get_queryset().get_or_create(status=self.status_filter, **kwargs)

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


def custom_email_validator(value):
    if not value.endswith('@example.com'):
        raise ValidationError(_('Invalid email address. Only example.com addresses are allowed.'))


class EmailConfirmation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    token = models.CharField(_("Token"), max_length=100, unique=True)
    created_at = models.DateTimeField(_("Created At"), default=timezone.now)
    is_confirmed = models.BooleanField(_("Is Confirmed"), default=False)

    def __str__(self):
        return f"EmailConfirmation for {self.user.username}"

    class Meta:
        verbose_name = _("Email Confirmation")
        verbose_name_plural = _("Email Confirmations")

    def clean(self):
        email_validator = EmailValidator(message="Invalid email address.")
        email_validator(self.user.email)  # This will raise a ValidationError if the email is invalid
        custom_email_validator(self.user.email)  # Custom validation

    def save(self, *args, **kwargs):
        self.clean()  # Run the custom validation before saving
        super().save(*args, **kwargs)

class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    token = models.CharField(_("Token"), max_length=100, unique=True)
    created_at = models.DateTimeField(_("Created At"), default=timezone.now)
    is_used = models.BooleanField(_("Is Used"), default=False)

    def __str__(self):
        return f"PasswordReset for {self.user.username}"

    class Meta:
        verbose_name = _("Password Reset")
        verbose_name_plural = _("Password Resets")


class EmailHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


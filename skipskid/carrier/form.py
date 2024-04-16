from django import forms
from .models import Carrier, CarrierAddress

class CarrierForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )

    class Meta:
        model = Carrier
        fields = ['name', 'about', 'contact_person', 'email', 'phone_number', 'website', 'pounds_plus', 'miles_plus']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match. Please enter matching passwords.")

        return cleaned_data

class CarrierAddressForm(forms.ModelForm):
    class Meta:
        model = CarrierAddress
        fields = ['line1', 'line2', 'city', 'state', 'postcode']
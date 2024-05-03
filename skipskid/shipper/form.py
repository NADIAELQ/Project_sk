from django import forms
from django.contrib.auth.models import User
from .models import Shipper, Business, Individual, BusinessAddress, IndividualAddress

class ShipperForm(forms.ModelForm):
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
        model = Shipper
        fields = ('email_address', 'password', 'confirm_password', 'name', 'phone_number', 'type')
        # fields = ('username', 'email', 'password', 'confirm_password', 'name', 'phone_number', 'type', 'contact_person', 'website')

    def __init__(self, *args, **kwargs):
        super(ShipperForm, self).__init__(*args, **kwargs)
        self.fields['email_address'].required = True

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email_address']  
        if commit:
            user.save()
            shipper_data = {field: self.cleaned_data[field] for field in ['name', 'phone_number', 'type']}
            shipper = Shipper(user=user, **shipper_data)
            shipper.save()
            if shipper.type == Shipper.BUSINESS:
                Business.objects.create(shipper=shipper, contact_person=self.cleaned_data['contact_person'], website=self.cleaned_data['website'])
            elif shipper.type == Shipper.INDIVIDUAL:
                Individual.objects.create(shipper=shipper)
        return user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match. Please enter matching passwords.")

        return cleaned_data

class ShipperAddressForm(forms.ModelForm):
    class Meta:
        if Shipper.type == Shipper.BUSINESS:
            model = BusinessAddress
        elif Shipper.type == Shipper.INDIVIDUAL:
            model = IndividualAddress
        fields = ['line1', 'line2', 'city', 'state', 'postcode']



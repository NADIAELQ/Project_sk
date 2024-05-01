from django.contrib import admin
from django import forms
from .models import Shipper, Business, Individual, BusinessAddress, IndividualAddress, TypeOfIndustry, TypeOfIndustry
                #  IndividualPreferredCarrier, ShipperEquipment, IndividualDelivery
from django.utils.translation import gettext_lazy as _


class BusinessAddressInline(admin.StackedInline):
    model = BusinessAddress
    verbose_name = "Address"
    icon = "location_on"
    fields = (
        ("line1", "line2"),
        ("city", "state"), 
        "postcode"
    )
    """
    no need for has_add_permission because of default_permissions set to False
    for all users
    """

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

class IndividualAddressInline(admin.StackedInline):
    model = IndividualAddress
    verbose_name = "Address"
    icon = "location_on"
    fields = (
        ("line1", "line2"),
        ("city", "state"), 
        "postcode"
    )
    """
    no need for has_add_permission because of default_permissions set to False
    for all users
    """

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

class TypeOfIndustryInline(admin.TabularInline):
    model = TypeOfIndustry
    verbose_name = "Typeofindustry"
    icon = "factory"
    extra = 0

    """
    no need for has_add_permission because of default_permissions set to False
    for all users
    """

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
# class PreferredCarrierInline(admin.StackedInline):
#     model = IndividualPreferredCarrier
#     verbose_name = "PreferredCarrier"
#     icon = "PreferredCarrier"
#     extra = 0
#     """
#     no need for has_add_permission because of default_permissions set to False
#     for all users
#     """

#     def has_change_permission(self, request, obj=None):
#         return request.user.is_superuser

#     def has_delete_permission(self, request, obj=None):
#         return request.user.is_superuser
    
# class IndividualDeliveryInline(admin.StackedInline):
#     model = IndividualDelivery
#     verbose_name = "IndividualDelivery"
#     icon = "IndividualDelivery"
#     extra = 0
#     """
#     no need for has_add_permission because of default_permissions set to False
#     for all users
#     """

#     def has_change_permission(self, request, obj=None):
#         return request.user.is_superuser

#     def has_delete_permission(self, request, obj=None):
#         return request.user.is_superuser

# class ShipperEquipmentInline(admin.StackedInline):
#     model = ShipperEquipment
#     verbose_name = "ShipperEquipment"
#     icon = "Forklift"
#     extra = 0
#     """
#     no need for has_add_permission because of default_permissions set to False
#     for all users
#     """

#     def has_change_permission(self, request, obj=None):
#         return request.user.is_superuser

#     def has_delete_permission(self, request, obj=None):
#         return request.user.is_superuser


# @admin.register(Business)
class BusinessInline(admin.StackedInline):
# class BusinessAdmin(admin.ModelAdmin):
    model = Business
    can_delete = False
    verbose_name_plural = 'Business'
    fk_name = 'shipper'
    fieldsets = (
        ('Basic Information', {
            'fields': ('type_of_industry', 'contact_person')
        }),
        ('Website and Media', {
            'fields': ('website', 'image')
        }),
        ('Facilities', {
            'fields': ('has_loading_dock', 'has_forklift', 'has_ramp')
        }),
    )


class IndividualInline(admin.StackedInline):
    model = Individual
    can_delete = False
    verbose_name_plural = 'Individual'
    fk_name = 'shipper'
    fieldsets = (
        ('Accessibility', {
            'fields': ('parking_available', 'easy_access_to_loading')
        }),
    )




# admin.site.register(PreferredCarrier, PreferredCarrierAdmin)
# admin.site.register(IndividualDelivery, IndividualDeliveryAdmin)
# admin.site.register(Business, BusinessAdmin)

class ShipperAdminForm(forms.ModelForm):
    class Meta:
        model = Shipper
        fields = '__all__'  

    # def __init__(self, *args, **kwargs):
    #     super(ShipperAdminForm, self).__init__(*args, **kwargs)
    #     instance = kwargs.get('instance')
    #     if instance:
    #         if instance.type == Shipper.BUSINESS:
    #             self.fields['business_specific_field'] = forms.CharField(required=False)
    #         elif instance.type == Shipper.INDIVIDUAL:
    #             self.fields['individual_specific_field'] = forms.CharField(required=False)

# @admin.register(Shipper)
class ShipperAdmin(admin.ModelAdmin):
    # exclude = ('user',)
    list_display = ['name', 'email_address', 'phone_number', 'shipper_type_display']
    search_fields = ['name', 'email_address']
    list_filter = ['type']
    # inlines = [BusinessInline, IndividualInline]
    inlines = []
    form = ShipperAdminForm

    def shipper_type_display(self, obj):
        return "Business" if obj.type == 'B' else "Individual"
    shipper_type_display.short_description = "Type of Shipper"

    # def shipper_type_display(self, obj):
    #     return "Business" if obj.type == Shipper.BUSINESS else "Individual"
    # shipper_type_display.short_description = "Type of Shipper"

    # def get_form(self, request, obj=None, **kwargs):
    #     Form = super(ShipperAdmin, self).get_form(request, obj, **kwargs)
    #     if obj:
    #         if obj.type == Shipper.BUSINESS:
    #             Form.base_fields['business_specific_field'] = forms.CharField(required=False)
    #         elif obj.type == Shipper.INDIVIDUAL:
    #             Form.base_fields['individual_specific_field'] = forms.CharField(required=False)
    #     return Form

    # def get_inline_instances(self, request, obj=None):
    #     inline_instances = []
    #     if obj is None:
    #         return inline_instances
    #     if obj.type == Shipper.BUSINESS:
    #         inline_instances.append(BusinessInline(self.model, self.admin_site))
    #     elif obj.type == Shipper.INDIVIDUAL:
    #         inline_instances.append(IndividualInline(self.model, self.admin_site))
    #     return inline_instances

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        # if obj:
        #     if obj.type == 'B':
        #         self.inlines = [BusinessInline, BusinessAddressInline]
        #     elif obj.type == 'I':
        #         self.inlines = [IndividualInline, IndividualAddressInline]
        self.inlines = [BusinessInline, BusinessAddressInline] if obj and obj.type == 'B' else [IndividualInline, IndividualAddressInline]
        return form


    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        if obj:
            if obj.type == 'B':
                inline_instances.extend([inline(self.model, self.admin_site) for inline in [BusinessInline, BusinessAddressInline]])
            elif obj.type == 'I':
                inline_instances.extend([inline(self.model, self.admin_site) for inline in [IndividualInline, IndividualAddressInline]])

        return inline_instances
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If this is a new object, there is no user yet
            # Create or select a user here
            # Example: obj.user = User.objects.create(...)
            pass
        super().save_model(request, obj, form, change)

admin.site.register(Shipper, ShipperAdmin)
    
admin.site.register(Business)
admin.site.register(Individual)













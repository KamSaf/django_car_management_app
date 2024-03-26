from django import forms
from .models import Workshop
from django.utils.safestring import mark_safe
from django.utils import timezone
from car_management_app.forms_utils import FormUtils


class WorkshopForm(forms.ModelForm, FormUtils):
    """
        Form for creating and editing workshops
    """

    def __init__(self, *args, **kwargs):
        self.logged_user = kwargs.pop('logged_user')
        super(WorkshopForm, self).__init__(*args, **kwargs)

    name = forms.Field(required=True, label=mark_safe('<i class="bi bi-person-vcard"></i> Workshop name'))
    city = forms.Field(required=True, label=mark_safe('<i class="bi bi-map"></i> City'))
    address = forms.Field(required=True, label=mark_safe('<i class="bi bi-geo-alt"></i> Address'))
    phone_number = forms.Field(required=True, label=mark_safe('<i class="bi bi-telephone"></i> Phone number'))
    profession = forms.Field(required=True, label=mark_safe('<i class="bi bi-wrench-adjustable-circle"></i> Workshop profession'))
    field_order = ['name', 'city', 'address', 'phone_number', 'profession']

    error_messages = {
        'field_too_long': "field value is too long.",
        'invalid_phone_number': "Provided phone number is invalid."
    }

    class Meta:
        model = Workshop
        fields = ['name', 'city', 'address', 'phone_number', 'profession']

    # sets initial value of fields
    def set_initial(self, workshop: Workshop = None):
        if workshop:
            self.initial['name'] = workshop.name
            self.initial['city'] = workshop.city
            self.initial['address'] = workshop.address
            self.initial['phone_number'] = workshop.phone_number
            self.initial['profession'] = workshop.profession
        return self

    def clean(self):
        MAX_STRING_FIELDS_LENGTH = 100
        name = self.cleaned_data.get('name')
        city = self.cleaned_data.get('city')
        address = self.cleaned_data.get('address')
        phone_number = self.cleaned_data.get('phone_number')
        profession = self.cleaned_data.get('profession')

        string_fields = [
            {'name': name},
            {'city': city},
            {'address': address},
            {'profession': profession},
        ]

        for i in range(len(string_fields)):
            if not WorkshopForm.check_field_length(value=list(string_fields[i].values())[0], length=MAX_STRING_FIELDS_LENGTH):
                self.length_error(field_name=list(string_fields[i].keys())[0].capitalize())
                return self.cleaned_data

        # checks if phone number field is valid
        if len(phone_number) != 9 or not phone_number.isdigit():
            self.data_errors['id_phone_number'] = self.error_messages['invalid_phone_number']
            self._errors['phone_number'] = self.error_class([self.error_messages["invalid_phone_number"]])
            return self.cleaned_data

        self.instance.name = name
        self.instance.city = city
        self.instance.address = address
        self.instance.phone_number = phone_number
        self.instance.profession = profession
        self.instance.user = self.logged_user
        self.instance.last_edit_date = timezone.now()

        if len(Workshop.objects.filter(user=self.logged_user)) == 0:
            self.instance.favourite = True

        return self.cleaned_data

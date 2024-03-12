from django import forms
from .models import Workshop
from django.utils.safestring import mark_safe
from django.utils import timezone


class WorkshopForm(forms.ModelForm):
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
    data_errors = {}
    field_order = ['name', 'city', 'address', 'phone_number', 'profession']

    error_messages = {
        'field_too_long': "field value is too long.",
        'invalid_phone_number': "Provided phone number is invalid."
    }

    class Meta:
        model = Workshop
        fields = ['name', 'city', 'address', 'phone_number', 'profession']

    def set_initial(self, workshop: Workshop = None):  # sets initial value of fields
        if workshop:
            self.initial['name'] = workshop.name
            self.initial['city'] = workshop.city
            self.initial['address'] = workshop.address
            self.initial['phone_number'] = workshop.phone_number
            self.initial['profession'] = workshop.profession
        return self

    def clear_errors(self):  # clears displayed error messages list
        self.data_errors = {}
        return self

    def clean(self):
        name = self.cleaned_data.get('name')
        city = self.cleaned_data.get('city')
        address = self.cleaned_data.get('address')
        phone_number = self.cleaned_data.get('phone_number')
        profession = self.cleaned_data.get('profession')

        if len(name) > 100:  # checks if workshop name field is proper length
            self.data_errors['id_name'] = self.error_messages['name_too_long']
            self._errors['name'] = self.error_class([f'Name {self.error_messages["field_too_long"]}'])
            return self.cleaned_data

        if len(city) > 100:  # checks if city field is proper length
            self.data_errors['id_city'] = self.error_messages['city_too_long']
            self._errors['city'] = self.error_class([f'City {self.error_messages["field_too_long"]}'])
            return self.cleaned_data

        if len(address) > 100:  # checks if address field is proper length
            self.data_errors['id_address'] = self.error_messages['address_too_long']
            self._errors['address'] = self.error_class([f'Address {self.error_messages["field_too_long"]}'])
            return self.cleaned_data

        if len(phone_number) != 9 or not phone_number.isdigit():  # checks if phone number field is valid
            self.data_errors['id_phone_number'] = self.error_messages['invalid_phone_number']
            self._errors['phone_number'] = self.error_class([self.error_messages["invalid_phone_number"]])
            return self.cleaned_data

        if len(profession) > 100:  # checks if profession field is proper length
            self.data_errors['id_profession'] = self.error_messages['profession_too_long']
            self._errors['profession'] = self.error_class([f'Profession {self.error_messages["field_too_long"]}'])
            return self.cleaned_data

        self.instance.name = name  # set name for new workshop
        self.instance.city = city  # set city for new workshop
        self.instance.address = address  # set address for new workshop
        self.instance.phone_number = phone_number  # set phone number for new workshop
        self.instance.profession = profession  # set profession for new workshop
        self.instance.user = self.logged_user  # set author user for new workshop
        self.instance.last_edit_date = timezone.now()

        if len(Workshop.objects.filter(user=self.logged_user)) == 0:
            self.instance.favourite = True

        return self.cleaned_data

from django import forms
from .models import Car
from django.utils.safestring import mark_safe
from cars.utils import populate_production_year_field
# from django.utils import timezone


class CarForm(forms.ModelForm):
    """
        Form for creating and editing cars
    """

    def __init__(self, *args, **kwargs):
        self.logged_user = kwargs.pop('logged_user')
        super(CarForm, self).__init__(*args, **kwargs)

    make = forms.Field(required=True, label=mark_safe('<i class="bi bi-person-vcard"></i> Make'))
    model = forms.Field(required=True, label=mark_safe('<i class="bi bi-map"></i> Model'))
    prod_year = forms.ChoiceField(required=False, label=mark_safe('<i class="bi bi-geo-alt"></i> Production year'), choices=populate_production_year_field())
    num_plate = forms.Field(required=False, label=mark_safe('<i class="bi bi-telephone"></i> Number plate'))
    fuel_type = forms.Field(required=False, label=mark_safe('<i class="bi bi-wrench-adjustable-circle"></i> Fuel type'))
    displacement = forms.IntegerField(required=False, label=mark_safe('<i class="bi bi-wrench-adjustable-circle"></i> Displacement (in cm3)'))
    vin = forms.Field(required=False, label=mark_safe('<i class="bi bi-wrench-adjustable-circle"></i> VIN number'))

    data_errors = {}
    field_order = ['make', 'model', 'prod_year', 'num_plate', 'fuel_type', 'displacement', 'vin']

    error_messages = {
        'field_too_long': "field value is too long.",
        'displacement_invalid': 'Invalid value in displacement field'
    }

    class Meta:
        model = Car
        fields = ['make', 'model', 'prod_year', 'num_plate', 'fuel_type', 'displacement', 'vin']

    def set_initial(self, car: Car = None):  # sets initial value of fields
        if car:
            self.initial['make'] = car.make
            self.initial['model'] = car.model
            self.initial['prod_year'] = car.prod_year
            self.initial['num_plate'] = car.num_plate
            self.initial['fuel_type'] = car.fuel_type
            self.initial['displacement'] = car.displacement
            self.initial['vin'] = car.vin
        return self

    def clear_errors(self):  # clears displayed error messages list
        self.data_errors = {}
        return self

    # def clean(self):
    #     make = self.cleaned_data.get('make')
    #     model = self.cleaned_data.get('model')
    #     # prod_year = self.cleaned_data.get('prod_year')
    #     num_plate = self.cleaned_data.get('num_plate')
    #     fuel_type = self.cleaned_data.get('fuel_type')
    #     displacement = self.cleaned_data.get('displacement')
    #     vin = self.cleaned_data.get('vin')


    #     if len(make) > 100:  # checks if car make field is proper length
    #         self.data_errors['id_make'] = self.error_messages['make_too_long']
    #         self._errors['make'] = self.error_class([f'Car make {self.error_messages["field_too_long"]}'])
    #         return self.cleaned_data

    #     if len(model) > 100:  # checks if car model field is proper length
    #         self.data_errors['id_model'] = self.error_messages['model_too_long']
    #         self._errors['model'] = self.error_class([f'Car model {self.error_messages["field_too_long"]}'])
    #         return self.cleaned_data


    #     ####

    #     # if len(prod) > 100:  # checks if address field is proper length
    #     #     self.data_errors['id_address'] = self.error_messages['address_too_long']
    #     #     self._errors['address'] = self.error_class([f'Address {self.error_messages["field_too_long"]}'])
    #     #     return self.cleaned_data

    #     ###

    #     if len(num_plate) > 50:  # checks if number plate field is proper length
    #         self.data_errors['id_num_plate'] = self.error_messages['num_plate_too_long']
    #         self._errors['num_plate'] = self.error_class([f'Number plate {self.error_messages["field_too_long"]}'])
    #         return self.cleaned_data

    #     if len(fuel_type) > 50:  # checks if fuel type field is proper length
    #         self.data_errors['id_fuel_type'] = self.error_messages['fuel_type_too_long']
    #         self._errors['fuel_type'] = self.error_class([f'Fuel type {self.error_messages["field_too_long"]}'])
    #         return self.cleaned_data

    #     if len(vin) > 25:  # checks if vin field is proper length
    #         self.data_errors['id_vin'] = self.error_messages['vin_too_long']
    #         self._errors['vin'] = self.error_class([f'VIN {self.error_messages["field_too_long"]}'])
    #         return self.cleaned_data

    #     if type(displacement) is not int or displacement < 0:  # checks if displacement field is valid
    #         self.data_errors['id_displacement'] = self.error_messages['displacement_invalid']
    #         self._errors['displacement'] = self.error_class([self.error_messages["displacement_invalid"]])
    #         return self.cleaned_data

    #     # self.instance.name = name  # set name for new workshop
    #     # self.instance.city = city  # set city for new workshop
    #     # self.instance.address = address  # set address for new workshop
    #     # self.instance.phone_number = phone_number  # set phone number for new workshop
    #     # self.instance.profession = profession  # set profession for new workshop
    #     # self.instance.user = self.logged_user  # set author user for new workshop
    #     # self.instance.last_edit_date = timezone.now()

    #     return self.cleaned_data

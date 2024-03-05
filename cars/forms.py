from django import forms
from .models import Car
from django.utils.safestring import mark_safe
from cars.utils import years_list
from django.utils import timezone


class CarForm(forms.ModelForm):
    """
        Form for creating and editing cars
    """

    def __init__(self, *args, **kwargs):
        self.logged_user = kwargs.pop('logged_user')
        super(CarForm, self).__init__(*args, **kwargs)

    make = forms.Field(required=True, label=mark_safe('<i class="bi bi-car-front"></i> Make'))
    model = forms.Field(required=True, label=mark_safe('<i class="bi bi-box"></i> Model'))
    prod_year = forms.ChoiceField(required=False, label=mark_safe('<i class="bi bi-calendar"></i> Production year'), choices=years_list())
    num_plate = forms.Field(required=False, label=mark_safe('<i class="bi bi-123"></i> Number plate'))
    fuel_type = forms.Field(required=False, label=mark_safe('<i class="bi bi-fuel-pump"></i> Fuel type'))
    displacement = forms.IntegerField(required=False, label=mark_safe('<i class="bi bi-arrows-angle-expand"></i> Displacement (in cm3)'))
    vin = forms.Field(required=False, label=mark_safe('<i class="bi bi-pencil-square"></i> VIN number'))

    data_errors = {}
    field_order = ['make', 'model', 'prod_year', 'num_plate', 'fuel_type', 'displacement', 'vin']

    error_messages = {
        'field_too_long': "field value is too long.",
        'displacement_invalid': 'Invalid displacement.',
        'production_year_invalid': 'Invalid production year.',
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

    def clean(self):
        make = self.cleaned_data.get('make')
        model = self.cleaned_data.get('model')
        prod_year = self.cleaned_data.get('prod_year')
        num_plate = self.cleaned_data.get('num_plate')
        fuel_type = self.cleaned_data.get('fuel_type')
        vin = self.cleaned_data.get('vin')

        try:
            displacement = int(self.cleaned_data.get('displacement'))
        except TypeError:
            self.data_errors['id_displacement'] = self.error_messages['displacement_invalid']
            self._errors['displacement'] = self.error_class([self.error_messages["displacement_invalid"]])

        if len(make) > 100:  # checks if make field is proper length
            self.data_errors['id_make'] = self.error_messages['make_too_long']
            self._errors['make'] = self.error_class([f'Make {self.error_messages["field_too_long"]}'])
            return self.cleaned_data

        if len(model) > 100:  # checks if model field is proper length
            self.data_errors['id_model'] = self.error_messages['model_too_long']
            self._errors['model'] = self.error_class([f'Model {self.error_messages["field_too_long"]}'])
            return self.cleaned_data

        if len(prod_year) not in years_list():  # checks if production year field is valid
            self.data_errors['id_prod_year'] = self.error_messages['invalid_production_year']
            self._errors['prod_year'] = self.error_class([self.error_messages['production_year_invalid']])
            return self.cleaned_data

        if len(num_plate) > 50:  # checks if number plate field is proper length
            self.data_errors['id_num_plate'] = self.error_messages['num_plate_too_long']
            self._errors['num_plate'] = self.error_class([f'Number plate {self.error_messages["field_too_long"]}'])
            return self.cleaned_data

        if len(fuel_type) > 50:  # checks if fuel type field is proper length
            self.data_errors['id_fuel_type'] = self.error_messages['fuel_type_too_long']
            self._errors['fuel_type'] = self.error_class([f'Fuel type {self.error_messages["field_too_long"]}'])
            return self.cleaned_data

        if len(vin) > 25:  # checks if vin field is proper length
            self.data_errors['id_vin'] = self.error_messages['vin_too_long']
            self._errors['vin'] = self.error_class([f'VIN {self.error_messages["field_too_long"]}'])
            return self.cleaned_data

        if displacement <= 0:  # checks if displacement field is valid
            self.data_errors['id_displacement'] = self.error_messages['displacement_invalid']
            self._errors['displacement'] = self.error_class([self.error_messages["displacement_invalid"]])
            return self.cleaned_data

        self.instance.make = make
        self.instance.model = model
        self.instance.prod_year = prod_year
        self.instance.num_plate = num_plate
        self.instance.fuel_type = fuel_type
        self.instance.vin = vin
        self.instance.displacement = displacement
        self.instance.last_edit_date = timezone.now()
        self.instance.create_date = timezone.now()
        self.instance.user = self.logged_user

        return self.cleaned_data

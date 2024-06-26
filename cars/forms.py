from django import forms
from .models import Car
from django.utils.safestring import mark_safe
from cars.utils import years_list
from django.utils import timezone
from car_management_app.forms_utils import FormUtils


class CarForm(forms.ModelForm, FormUtils):
    """
        Form for creating and editing cars
    """

    def __init__(self, *args, **kwargs):
        self.logged_user = kwargs.pop('logged_user')
        super(CarForm, self).__init__(*args, **kwargs)

    make = forms.Field(required=True, label=mark_safe('<i class="bi bi-car-front"></i> Make'))
    model = forms.Field(required=True, label=mark_safe('<i class="bi bi-box"></i> Model'))
    prod_year = forms.ChoiceField(required=False, label=mark_safe('<i class="bi bi-calendar"></i> Production year'), choices=years_list())
    num_plate = forms.Field(required=True, label=mark_safe('<i class="bi bi-123"></i> Number plate'))
    fuel_type = forms.Field(required=False, label=mark_safe('<i class="bi bi-fuel-pump"></i> Fuel type'))
    displacement = forms.IntegerField(required=False, label=mark_safe('<i class="bi bi-arrows-angle-expand"></i> Displacement (in cm3)'))
    vin = forms.Field(required=False, label=mark_safe('<i class="bi bi-pencil-square"></i> VIN number'))

    field_order = ['make', 'model', 'prod_year', 'num_plate', 'fuel_type', 'displacement', 'vin']

    error_messages = {
        'field_too_long': "field value is too long.",
        'displacement_invalid': 'Invalid displacement.',
        'production_year_invalid': 'Invalid production year.',
        'blank_fields': 'Required fields must not be blank',
    }

    class Meta:
        model = Car
        fields = ['make', 'model', 'prod_year', 'num_plate', 'fuel_type', 'displacement', 'vin']

    # sets initial value of fields
    def set_initial(self, car: Car = None):
        if car:
            self.initial['make'] = car.make
            self.initial['model'] = car.model
            self.initial['prod_year'] = car.prod_year
            self.initial['num_plate'] = car.num_plate
            self.initial['fuel_type'] = car.fuel_type
            self.initial['displacement'] = car.displacement
            self.initial['vin'] = car.vin
        return self

    def clean(self):
        STRING_FIELDS_LENGTHS = [100, 100, 50, 50, 25]
        make = self.cleaned_data.get('make')
        model = self.cleaned_data.get('model')
        num_plate = self.cleaned_data.get('num_plate')
        prod_year = self.cleaned_data.get('prod_year')
        fuel_type = self.cleaned_data.get('fuel_type')
        vin = self.cleaned_data.get('vin')

        if None in [make, model, vin]:
            error = self.error_messages['blank_fields']
            self.data_errors['required_fields'] = error
            self._errors['required_fields'] = self.error_class([error])
            return self.cleaned_data

        string_fields = [
            {'make': make},
            {'model': model},
            {'num_plate': num_plate},
            {'fuel_type': fuel_type},
            {'vin': vin}
        ]

        for i in range(len(string_fields)):
            if not CarForm.check_field_length(value=list(string_fields[i].values())[0], length=STRING_FIELDS_LENGTHS[i]):
                dict_key = list(string_fields[i].keys())[0]
                field_name = dict_key.upper() if dict_key == 'vin' else dict_key.capitalize()
                self.length_error(field_name=field_name)
                return self.cleaned_data

        try:
            displacement = int(self.cleaned_data.get('displacement'))
        except TypeError:
            displacement_error = self.error_messages['displacement_invalid']
            self.data_errors['id_displacement'] = displacement_error
            self._errors['displacement'] = self.error_class([displacement_error])
            return self.cleaned_data

        # checks if production year field is valid
        prod_year_options = [option[1] for option in years_list()]
        if prod_year not in prod_year_options:
            prod_year_error = self.error_messages['invalid_production_year']
            self.data_errors['id_prod_year'] = prod_year_error
            self._errors['prod_year'] = self.error_class([prod_year_error])
            return self.cleaned_data

        # checks if displacement field is valid
        if displacement <= 0:
            displacement_error = self.error_messages['displacement_invalid']
            self.data_errors['id_displacement'] = displacement_error
            self._errors['displacement'] = self.error_class([displacement_error])
            return self.cleaned_data

        self.instance.make = make
        self.instance.model = model
        self.instance.prod_year = prod_year
        self.instance.num_plate = num_plate
        self.instance.fuel_type = fuel_type
        self.instance.vin = vin
        self.instance.displacement = displacement
        self.instance.last_edit_date = timezone.now()
        self.instance.user = self.logged_user

        return self.cleaned_data

from django import forms
from .models import Entry
from django.utils.safestring import mark_safe
from django.utils import timezone
from car_management_app.forms_utils import FormUtils


class EntryForm(forms.ModelForm, FormUtils):
    """
        Form for creating and editing exploitation history entries
    """

    category = forms.ChoiceField(required=True, label=mark_safe('<i class="bi bi-boxes"></i> Category'), choices=Entry.TYPES_OF_ENTRIES)
    place = forms.Field(required=False, label=mark_safe('<i class="bi bi-geo-alt"></i> Place'))
    mileage = forms.Field(required=True, label=mark_safe('<i class="bi bi-activity"></i> Mileage'))
    cost = forms.Field(required=True, label=mark_safe('<i class="bi bi-currency-dollar"></i> Cost'))
    details = forms.Field(required=False, label=mark_safe('<i class="bi bi-card-text"></i> Details'), widget=forms.Textarea(attrs={"rows": "5"}))
    fuel_liters = forms.FloatField(required=False, label=mark_safe('<i class="bi bi-fuel-pump"></i> Fuel liters (for Fuel entries)'))

    field_order = ['date', 'category', 'place', 'mileage', 'cost', 'fuel_liters', 'details']

    error_messages = {
        'field_value_too_long': 'field value is too long.',
        'mileage_smaller': 'Mileage cannot be smaller than in an entry before it.',
        'mileage_bigger': 'Mileage cannot be bigger than in an entry after it.',
        'date_error': 'Entry date must not be in the future.',
        'negative_value': 'Field value can not be negative value.',
        'blank_fields': 'Required fields must not be blank',
    }

    class Meta:
        model = Entry
        fields = ['date', 'category', 'place', 'mileage', 'details', 'cost', 'fuel_liters']
        widgets = {
            'date': forms.widgets.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.logged_user = kwargs.pop('logged_user')
        self.request = kwargs.pop('request', None)
        self.car = kwargs.pop('car')
        super(EntryForm, self).__init__(*args, **kwargs)

    # sets initial value of fields
    def set_initial(self, entry: Entry = None):
        if entry:
            self.initial['category'] = entry.make
            self.initial['place'] = entry.model
            self.initial['mileage'] = entry.prod_year
            self.initial['cost'] = entry.num_plate
            self.initial['details'] = entry.fuel_type
        return self

    def clean(self):
        category = self.cleaned_data.get('category')
        place = self.cleaned_data.get('place')
        details = self.cleaned_data.get('details')
        date = self.cleaned_data.get('date')

        if self.cleaned_data.get('fuel_liters'):
            # check if type of fuel_liters is valid
            try:
                fuel_liters = int(float(self.cleaned_data.get('fuel_liters')))
            except TypeError:
                fuel_error = EntryForm.invalid_field_value(field_name='fuel_liters')
                self.data_errors['id_fuel_liters'] = fuel_error
                self._errors['fuel_liters'] = self.error_class(fuel_error)
                return self.cleaned_data

            # check if fuel_liters is not negative
            if fuel_liters < 0:
                fuel_error = self.error_messages['negative_value']
                self.data_errors['id_fuel_liters'] = fuel_error
                self._errors['fuel_liters'] = self.error_class(fuel_error)
                return self.cleaned_data

            self.instance.fuel_liters = fuel_liters
        else:
            self.instance.fuel_liters = None

        # check if given date is not in the future
        if date > timezone.now():
            date_error = self.error_messages['date_error']
            self.data_errors['id_date'] = date_error
            self._errors['date'] = self.error_class(date_error)
            return self.cleaned_data

        # check if type of cost is valid
        try:
            cost = int(float(self.cleaned_data.get('cost')))
        except TypeError:
            cost_error = EntryForm.invalid_field_value(field_name='cost')
            self.data_errors['id_cost'] = cost_error
            self._errors['cost'] = self.error_class(cost_error)
            return self.cleaned_data

        # check if type of mileage is valid
        try:
            mileage = int(self.cleaned_data.get('mileage'))
        except TypeError:
            mileage_error = EntryForm.invalid_field_value(field_name='mileage')
            self.data_errors['id_mileage'] = mileage_error
            self._errors['mileage'] = self.error_class(mileage_error)
            return self.cleaned_data

        if None in [date, category, mileage, cost]:
            error = self.error_messages['blank_fields']
            self._errors['required_fields'] = self.error_class([error])
            return self.cleaned_data

        # check if cost is not negative
        if cost < 0:
            cost_error = self.error_messages['negative_value']
            self.data_errors['id_cost'] = cost_error
            self._errors['cost'] = self.error_class(cost_error)
            return self.cleaned_data

        entries = Entry.objects.filter(car=self.car).exclude(id=self.instance.id).order_by('-date').all()

        # check if mileage is not negative
        if mileage < 0:
            mileage_error = self.error_messages['negative_value']
            self.data_errors['id_mileage'] = mileage_error
            self._errors['mileage'] = self.error_class(mileage_error)
            return self.cleaned_data

        # check if mileage field value is smaller than in last saved entry
        last_entry = entries.filter(date__lt=date).order_by('-date').first()
        if last_entry and last_entry.mileage > mileage:
            mileage_error = self.error_messages['mileage_smaller']
            self.data_errors['id_mileage'] = mileage_error
            self._errors['mileage'] = mileage_error
            return self.cleaned_data

        # check if mileage field value is bigger than in "next" saved entry (when editing one of old entries)
        newer_entry = entries.filter(date__gt=date).order_by('-date').first()
        if newer_entry and newer_entry.mileage < mileage:
            mileage_error = self.error_messages['mileage_bigger']
            self.data_errors['id_mileage'] = mileage_error
            self._errors['mileage'] = mileage_error
            return self.cleaned_data

        # check if category field value is valid
        if category not in Entry.TYPES_OF_ENTRIES:
            category_error = EntryForm.invalid_field_value(field_name='category')
            self.data_errors['id_category'] = category_error
            self._errors['category'] = category_error
            return self.cleaned_data

        # check if place field value is not too long
        if not EntryForm.check_field_length(value=place, length=200):
            self.length_error(field_name='Place')
            return self.cleaned_data

        # check if details field value is not too long
        if not EntryForm.check_field_length(value=details, length=500):
            self.length_error(field_name='Details')
            return self.cleaned_data

        self.instance.category = category
        self.instance.place = place
        self.instance.details = details
        self.instance.cost = cost
        self.instance.mileage = mileage
        self.instance.last_edit_date = timezone.now()
        self.instance.user = self.logged_user
        self.instance.car = self.car

        return self.cleaned_data

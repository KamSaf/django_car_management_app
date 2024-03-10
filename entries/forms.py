from django import forms
from .models import Entry
from django.utils.safestring import mark_safe
from django.utils import timezone


class EntryForm(forms.ModelForm):
    """
        Form for creating and editing exploitation history entries
    """

    category = forms.ChoiceField(required=True, label=mark_safe('Category'), choices=Entry.TYPES_OF_ENTRIES)
    place = forms.Field(required=False, label=mark_safe('Place'))
    mileage = forms.Field(required=True, label=mark_safe('Mileage'))
    cost = forms.Field(required=True, label=mark_safe('Cost'))
    details = forms.Field(required=False, label=mark_safe('Details'), widget=forms.Textarea(attrs={"rows": "5"}))

    data_errors = {}
    field_order = ['date', 'category', 'place', 'mileage', 'cost', 'details']

    error_messages = {
        'field_value_too_long': 'field value is too long.',
        'mileage_smaller': 'Mileage cannot be smaller than in an entry before it.',
        'date_error': 'Entry date must not be in the future.',
    }

    class Meta:
        model = Entry
        fields = ['date', 'category', 'place', 'mileage', 'details', 'cost']
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

    # clears displayed error messages list
    def clear_errors(self):
        self.data_errors = {}
        return self

    # returns error message for invalid value name
    def __invalid_field_value(field_name: str) -> str:
        return f'Invalid {field_name} field value.'

    def clean(self):
        category = self.cleaned_data.get('category')
        place = self.cleaned_data.get('place')
        details = self.cleaned_data.get('details')
        date = self.cleaned_data.get('date')

        # check if given date is not in the future
        if date > timezone.now():
            date_error = self.error_messages['date_error']
            self.data_errors['id_date'] = date_error
            self._errors['date'] = self.error_class(date_error)
            return self.cleaned_data

        # check if type of cost is valid
        try:
            cost = int(self.cleaned_data.get('cost'))
        except TypeError:
            cost_error = EntryForm.__invalid_field_value(field_name='cost')
            self.data_errors['id_cost'] = cost_error
            self._errors['cost'] = self.error_class(cost_error)
            return self.cleaned_data

        # check if type of mileage is valid
        try:
            mileage = int(self.cleaned_data.get('mileage'))
        except TypeError:
            mileage_error = EntryForm.__invalid_field_value(field_name='mileage')
            self.data_errors['id_mileage'] = mileage_error
            self._errors['mileage'] = self.error_class(mileage_error)
            return self.cleaned_data

        # check if mileage field value is smaller than in last saved entry
        last_entry = Entry.objects.filter(user=self.logged_user, date__lte=date).exclude(id=self.instance.id).order_by('-date').first()
        if last_entry and last_entry.mileage > mileage:
            mileage_error = self.error_messages['mileage_smaller']
            self.data_errors['id_mileage'] = mileage_error
            self._errors['mileage'] = mileage_error
            return self.cleaned_data

        # check if category field value is valid
        if category not in Entry.TYPES_OF_ENTRIES:
            category_error = EntryForm.__invalid_field_value(field_name='category')
            self.data_errors['id_category'] = category_error
            self._errors['category'] = category_error
            return self.cleaned_data

        # check if place field value is not too long
        if len(place) > 200:
            place_error = 'Place ' + self.error_messages['field_value_too_long']
            self.data_errors['id_place'] = place_error
            self._errors['place'] = place_error
            return self.cleaned_data

        # check if details field value is not too long
        if len(details) > 1024:
            details_error = 'Details ' + self.error_messages['field_value_too_long']
            self.data_errors['id_details'] = details_error
            self._errors['details'] = details_error
            return self.cleaned_data

        self.instance.category = category
        self.instance.place = place
        self.instance.details = details
        self.instance.cost = cost
        self.instance.mileage = mileage
        self.instance.last_edit_date = timezone.now()
        self.instance.create_date = timezone.now()
        self.instance.user = self.logged_user
        self.instance.car = self.car

        return self.cleaned_data
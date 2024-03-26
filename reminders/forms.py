from django import forms
from .models import Reminder
from entries.models import Entry
from django.utils.safestring import mark_safe
from django.utils import timezone
from car_management_app.forms_utils import FormUtils


class ReminderForm(forms.ModelForm, FormUtils):
    """
        Form for creating and editing reminders
    """

    category = forms.ChoiceField(required=True, label=mark_safe('<i class="bi bi-boxes"></i> Category'), choices=Entry.TYPES_OF_ENTRIES)
    place = forms.Field(required=False, label=mark_safe('<i class="bi bi-geo-alt"></i> Place'))
    details = forms.Field(required=True, label=mark_safe('<i class="bi bi-card-text"></i> Details'), widget=forms.Textarea(attrs={"rows": "5"}))

    field_order = ['date', 'category', 'place', 'details']

    error_messages = {
        'field_value_too_long': 'field value is too long.',
        'date_error': 'Entry date must not be in the past.',
    }

    class Meta:
        model = Reminder
        fields = ['date', 'category', 'place', 'details']
        widgets = {
            'date': forms.widgets.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.logged_user = kwargs.pop('logged_user')
        self.car = kwargs.pop('car')
        super(ReminderForm, self).__init__(*args, **kwargs)

    # sets initial value of fields
    def set_initial(self, entry: Entry = None):
        if entry:
            self.initial['category'] = entry.make
            self.initial['place'] = entry.model
            self.initial['details'] = entry.fuel_type
        return self

    def clean(self):
        category = self.cleaned_data.get('category')
        place = self.cleaned_data.get('place')
        details = self.cleaned_data.get('details')
        date = self.cleaned_data.get('date')

        # check if given date is not in the past
        if date < timezone.now():
            date_error = self.error_messages['date_error']
            self.data_errors['id_date'] = date_error
            self._errors['date'] = self.error_class(date_error)
            return self.cleaned_data

        # check if category field value is valid
        if category not in Entry.TYPES_OF_ENTRIES:
            category_error = ReminderForm.invalid_field_value(field_name='category')
            self.data_errors['id_category'] = category_error
            self._errors['category'] = category_error
            return self.cleaned_data

        # check if place field value is not too long
        if not ReminderForm.check_field_length(value=place, length=200):
            self.length_error(field_name='Place')
            return self.cleaned_data

        # check if details field value is not too long
        if not ReminderForm.check_field_length(value=details, length=100):
            self.length_error(field_name='Details')
            return self.cleaned_data

        self.instance.category = category
        self.instance.place = place
        self.instance.details = details
        self.instance.last_edit_date = timezone.now()
        self.instance.user = self.logged_user
        self.instance.car = self.car

        return self.cleaned_data

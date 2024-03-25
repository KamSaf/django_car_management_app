from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password, make_password
from car_management_app.forms_utils import FormUtils
from django.contrib.auth import update_session_auth_hash


class UserRegisterForm(UserCreationForm):
    """
        Form for registering new user
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm, FormUtils):
    """
        Form for editing user data
    """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(UserUpdateForm, self).__init__(*args, **kwargs)

    error_messages = {
        'field_too_long': "field value is too long.",
        'wrong_password': "Provided current password is not valid.",
        'passwords_mismatch': "New passwords fields don't match.",
        'same_password': "New password is identical to the current one.",
        'duplicate_email': "This email is already taken.",
        'duplicate_username': "This username is already taken.",
        'password_not_confirmed': "You need to enter new password in two fields.",
    }

    email = forms.EmailField(required=True, label='New email address')
    name = forms.Field(required=False, label='New name')
    new_password1 = forms.Field(widget=forms.PasswordInput(), required=False, label='New password')
    new_password2 = forms.Field(widget=forms.PasswordInput(), required=False, label='Confirm new password')
    current_password = forms.Field(widget=forms.PasswordInput(), label='Current password')
    data_errors = {}
    field_order = ['email', 'name', 'username', 'new_password1', 'new_password2', 'current_password']

    class Meta:
        model = User
        fields = ['email', 'username', 'new_password1', 'new_password2', 'current_password']

    # sets initial value for email, username and name fields as current user data
    def set_initial(self, user: User = None):
        if user:
            self.initial['email'] = user.email
            self.initial['username'] = user.username
            self.initial['name'] = user.first_name
        return self

    def clean(self):
        STRING_FIELDS_LENGTHS = [150, 150, 150, 254]
        current_password = self.cleaned_data.get('current_password')
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        new_email = self.cleaned_data.get('email')
        new_username = self.cleaned_data.get('username')
        new_name = self.cleaned_data.get('name')

        string_fields = [
            {'username': new_username},
            {'name': new_name},
            {'email': new_email},
            {'new_password1': new_password1},
        ]

        for i in range(len(string_fields)):
            if not UserUpdateForm.check_field_length(value=list(string_fields[i].values())[0], length=STRING_FIELDS_LENGTHS[i]):
                field_name = list(string_fields[i].keys())[0].capitalize()
                self.set_length_errors(field_name=field_name)
                return self.cleaned_data

        # checks if user provided valid password (current)
        if not check_password(current_password, self.instance.password):
            self.data_errors['id_current_password'] = self.error_messages['wrong_password']
            self._errors['current_password'] = self.error_class([self.error_messages['wrong_password']])
            return self.cleaned_data

        # checks if provided new passwords are the same
        if new_password1 and new_password2:
            if new_password1 != new_password2:
                self.data_errors['id_new_password1'] = self.error_messages['passwords_mismatch']
                self.data_errors['id_new_password2'] = ''
                self._errors['new_password1'] = self.error_class([self.error_messages['passwords_mismatch']])
                return self.cleaned_data

            # checks if provided new password is identical to the current one
            if check_password(new_password1, self.instance.password):
                self.data_errors['id_new_password1'] = self.error_messages['same_password']
                self.data_errors['id_new_password2'] = ''
                self._errors['new_password1'] = self.error_class([self.error_messages['same_password']])
                return self.cleaned_data

        # checks if both new password fields are filled
        if (new_password1 and not new_password2) or (new_password2 and not new_password1):
            self.data_errors['id_new_password1'] = self.error_messages['password_not_confirmed']
            self.data_errors['id_new_password2'] = ''
            self._errors['new_password1'] = self.error_class([self.error_messages['password_not_confirmed']])
            return self.cleaned_data

        # checks if provided new email is already taken
        user_by_email = User.objects.filter(email=new_email).first()
        if user_by_email and user_by_email.id != self.instance.id:
            self.data_errors['id_email'] = self.error_messages['duplicate_email']
            self._errors['email'] = self.error_class([self.error_messages['duplicate_email']])
            return self.cleaned_data

        # checks if provided new username is already taken
        user_by_username = User.objects.filter(username=new_username).first()
        if user_by_username and user_by_username.id != self.instance.id:
            self.data_errors['id_username'] = self.error_messages['duplicate_username']
            self._errors['username'] = self.error_class([self.error_messages['duplicate_username']])
            return self.cleaned_data

        self.instance.email = new_email
        self.instance.username = new_username

        if new_password1:
            self.instance.password = make_password(new_password1)
            update_session_auth_hash(self.request, self.request.user)

        if new_name:
            self.instance.first_name = new_name

        return self.cleaned_data

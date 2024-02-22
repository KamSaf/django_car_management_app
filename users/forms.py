from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password, make_password


class UserRegisterForm(UserCreationForm):
    """
        Form for registering new user
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    """
        Form for editing user data
    """

    error_messages = {
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
    data_errors = []
    field_order = ['email', 'name', 'username', 'new_password1', 'new_password2', 'current_password']

    class Meta:
        model = User
        fields = ['email', 'username', 'new_password1', 'new_password2', 'current_password']

    def set_initial(self, user: User = None):  # sets initial value for email, username and name fields as current user data
        self.initial['email'] = user.email
        self.initial['username'] = user.username
        self.initial['first_name'] = user.first_name
        return self

    def clear_errors(self):  # clears displayed error messages list
        self.data_errors = []
        return self

    def clean(self):
        current_password = self.cleaned_data.get('current_password')
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        new_email = self.cleaned_data.get('email')
        new_username = self.cleaned_data.get('username')
        new_name = self.cleaned_data.get('name')

        if not check_password(current_password, self.instance.password):  # checks if user provided valid password (current)
            self.data_errors.append(self.error_messages['wrong_password'])
            self._errors['current_password'] = self.error_class([self.error_messages['wrong_password']])
            return self.cleaned_data

        if new_password1 and new_password2:
            if new_password1 != new_password2:  # checks if provided new passwords are the same
                self.data_errors.append(self.error_messages['passwords_mismatch'])
                self._errors['new_password1'] = self.error_class([self.error_messages['passwords_mismatch']])
                return self.cleaned_data

            if check_password(new_password1, self.instance.password):  # checks if provided new password is identical to the current one
                self.data_errors.append(self.error_messages['same_password'])
                self._errors['new_password1'] = self.error_class([self.error_messages['same_password']])
                return self.cleaned_data

            self.instance.password = make_password(new_password1)  # set new password for user

        if (new_password1 and not new_password2) or (new_password2 and not new_password1):  # checks if both new password fields are filled
            self.data_errors.append(self.error_messages['password_not_confirmed'])
            self._errors['new_password1'] = self.error_class([self.error_messages['password_not_confirmed']])
            return self.cleaned_data

        user_by_email = User.objects.filter(email=new_email).first()
        if user_by_email and user_by_email.id != self.instance.id:  # checks if provided new email is already taken
            self.data_errors.append(self.error_messages['duplicate_email'])
            self._errors['email'] = self.error_class([self.error_messages['duplicate_email']])
            return self.cleaned_data

        user_by_username = User.objects.filter(username=new_username).first()  # checks if provided new username is already taken
        if user_by_username and user_by_username.id != self.instance.id:
            self.data_errors.append(self.error_messages['duplicate_username'])
            self._errors['username'] = self.error_class([self.error_messages['duplicate_username']])
            return self.cleaned_data

        self.instance.email = new_email  # set new email for user
        self.instance.username = new_username  # set new username for user

        if new_name:
            self.instance.first_name = new_name  # set new name for user

        return self.cleaned_data

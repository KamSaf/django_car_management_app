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
        'same_password': "New password is identical to the current one."
    }

    email = forms.EmailField(required=True)
    new_password1 = forms.Field(widget=forms.PasswordInput(), required=False)
    new_password2 = forms.Field(widget=forms.PasswordInput(), required=False)
    current_password = forms.Field(widget=forms.PasswordInput())
    data_errors = []

    class Meta:
        model = User
        fields = ['email', 'username', 'new_password1', 'new_password2', 'current_password']

    def set_initial(self, user: User = None):
        self.initial['email'] = user.email
        self.initial['username'] = user.username
        return self

    def clear_errors(self):
        self.data_errors = []
        return self

    def clean(self):
        current_password = self.cleaned_data.get('current_password')
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')

        print(f'\n\n\n {check_password(current_password, self.instance.password)} \n\n')
        if not check_password(current_password, self.instance.password):
            self.data_errors.append(self.error_messages['wrong_password'])
        if new_password1 and new_password2:
            if new_password1 != new_password2:
                self.data_errors.append(self.error_messages['passwords_mismatch'])
            elif check_password(new_password1, self.instance.password):
                self.data_errors.append(self.error_messages['same_password'])
            else:
                self.instance.password = make_password(new_password1)
        self.instance.username = self.cleaned_data
        return self.cleaned_data

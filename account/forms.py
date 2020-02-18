from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import Account

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, widget=forms.EmailInput(attrs={"placeholder": "Email address"}))

    class Meta:
        model = Account
        fields = ("email", "full_name", "username", "password1", "password2")
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Full Name"}),
            "username": forms.TextInput(attrs={"placeholder": "Username"}),
        }

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Password Again'})


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Password"
    }))

    class Meta:
        model  = Account
        fields = ('email', 'password')
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "Email Address"})
        }

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")
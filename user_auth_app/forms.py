from django import forms
from .models import CustomUser
from django.core import validators

import datetime
import random
import hashlib


class RegistrationForm(forms.ModelForm):
    
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput(attrs={'class':'form-control',
                                                                  'required': ''}))
    password2 = forms.CharField(label="Repeat password",
                                widget=forms.PasswordInput(attrs={'class':'form-control',
                                                                  'required': ''}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control', 'required' : ''})
        self.fields['email'].widget.attrs.update({'class':'form-control', 'required' : ''})
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords are not equal.")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return username
        raise validators.ValidationError("User with this username already exists.")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return email
        raise validators.ValidationError("User with this email already exists.")

    def _generate_activation_key(self):
        salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
        return hashlib.sha1((salt+self.cleaned_data['email']).encode('utf-8')).hexdigest()

    @staticmethod
    def _generate_key_expires(days=2):
        return datetime.datetime.today() + datetime.timedelta(days)

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)

        # generate email activation key data
        user.activation_key = self._generate_activation_key()
        user.key_expires = self._generate_key_expires()

        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.is_active = False
            user.save()
        return user

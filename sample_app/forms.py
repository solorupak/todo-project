from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.utils.html import mark_safe

from .models import *

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
    'class': 'form-control',
    'required': 'true',
    'placeholder': 'Password *'}))
    
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'required': 'true',
        'placeholder': 'Retype Password *'}))

    class Meta:
        model = User
        fields = ('username','first_name','last_name', 'email', 'password', 'confirm_password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['first_name'].widget.attrs.update({'placeholder':'First Name'})
        self.fields['last_name'].widget.attrs.update({'placeholder':'Last Name'})
        self.fields['username'].widget.attrs.update({'placeholder':'Username'})
        self.fields['email'].label="Email"
        self.fields['password'].label="Password"
        self.fields['confirm_password'].label="Confirm Password"



    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if not confirm_password:
            raise forms.ValidationError("You must confirm your password")
        if password != confirm_password:
            raise forms.ValidationError("Your passwords do not match")

        return confirm_password

    def clean_email(self):
        data = self.cleaned_data['email']
        if not data:
            raise forms.ValidationError("Email cannot be Empty")
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError(mark_safe("<span style='color: red;'>User with this email already exists</span>"))

        # Always return the cleaned data, whether you have changed it or
        # not.
        return data



class LoginForm(forms.Form):
	username = forms.CharField(
		widget=forms.TextInput(
			attrs={'class': 'form-control', 'placeholder':  'Username'}))
	password = forms.CharField(
		widget=forms.PasswordInput(
			attrs={'class': 'form-control', 'placeholder':  'Password'}))


class DesignationForm(forms.ModelForm):

    class Meta:
        model = Designation
        fields = ['name','position']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update(
                {'class': 'form-control'})


class DesignationDeleteForm(forms.ModelForm):
    
    class Meta:
        model = Designation 
        fields = ['deleted_at']
        widgets = {
        'deleted_at': forms.HiddenInput(),
        }

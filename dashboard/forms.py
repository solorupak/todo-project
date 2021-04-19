from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.utils.html import mark_safe

from .models import User, Designation

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
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'confirm_password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

        self.fields['first_name'].widget.attrs.update({'placeholder':'First Name'})
        self.fields['last_name'].widget.attrs.update({'placeholder':'Last Name'})
        self.fields['username'].widget.attrs.update({'placeholder':'Username'})
        self.fields['email'].label = "Email"
        self.fields['password'].label = "Password"
        self.fields['confirm_password'].label = "Confirm Password"



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

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.filter(username=username, is_active=True).first()
        if user == None or not user.check_password(password):
            raise forms.ValidationError("Incorrect username or password")
        return self.cleaned_data

class PasswordResetForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder':  'Current Password'}))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder':  'Password'}))
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder':  'Confirm Password'}))

    def set_user(self, user):
        self.user = user
    
    def clean(self):
        current_password = self.cleaned_data.get('current_password')
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        user = self.user
        if not user.check_password(current_password):
            raise forms.ValidationError({"current_password": "Incorrect password" })
        if not confirm_password:
            raise forms.ValidationError({'corfirm_password': "You must confirm your password" })
        if password != confirm_password:
            raise forms.ValidationError({'confirm_password': "Your passwords do not match" })

        return self.cleaned_data


class DesignationForm(forms.ModelForm):

    class Meta:
        model = Designation
        fields = ['name', 'position', 'gender', 'date_of_birth']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['date_of_birth'].widget.attrs.update({
            'class': 'form-control datetimepicker'
        })
        self.fields['gender'].widget.attrs.update({
            'class': 'form-control select2'
        })


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
    
    def clean_email(self):
        email =  self.cleaned_data.get('email')

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("User with this email address already exists")
        
        return email

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['job'].widget.attrs['rows'] = '4'
        self.fields['job'].widget.attrs['placeholder'] = 'Tell us about your Job'
        self.fields['job'].widget.attrs['id'] = '1'
        self.fields['education'].widget.attrs['rows'] = '4'
        self.fields['education'].widget.attrs['placeholder'] = 'Tell us about your Education'
        self.fields['education'].widget.attrs['id'] = '2'
        self.fields['projects'].widget.attrs['rows'] = '4'
        self.fields['projects'].widget.attrs['placeholder'] = 'Tell us about your Projects'
        self.fields['projects'].widget.attrs['id'] = '3'
        self.fields['skills'].widget.attrs['rows'] = '4'
        self.fields['skills'].widget.attrs['placeholder'] = 'Tell us about your Skills'
        self.fields['skills'].widget.attrs['id'] = '4'
        self.fields['internships'].widget.attrs['rows'] = '4'
        self.fields['internships'].widget.attrs['placeholder'] = 'Tell us about your Internships'
        self.fields['internships'].widget.attrs['id'] = '5'
        self.fields['links'].widget.attrs['rows'] = '4'
        self.fields['links'].widget.attrs['placeholder'] = 'Drop any Links which contains your work'
        self.fields['links'].widget.attrs['id'] = '6'

    class Meta:
        model = Profile
        fields = ['image','job','education','projects','skills','internships','links']
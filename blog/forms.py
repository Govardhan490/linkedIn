from django import forms
from users.models import Profile

class ProfileViewForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfileViewForm, self).__init__(*args, **kwargs)
        self.fields['job'].widget.attrs['id'] = '1'
        self.fields['education'].widget.attrs['id'] = '2'
        self.fields['projects'].widget.attrs['id'] = '3'
        self.fields['skills'].widget.attrs['id'] = '4'
        self.fields['internships'].widget.attrs['id'] = '5'
        self.fields['links'].widget.attrs['id'] = '6'

    class Meta:
        model = Profile
        fields = ['job','education','projects','skills','internships','links']
from django import forms
from . models import User, UserProfile
from .validators import allow_only_images_validators


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': ''
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': ''
    }))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = ''
        self.fields['last_name'].widget.attrs['placeholder'] = ''
        self.fields['username'].widget.attrs['placeholder'] = ''
        self.fields['email'].widget.attrs['placeholder'] = ''
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'password does not match!'
            )

class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget = forms.TextInput(attrs={'class': '', 'required': 'required'}))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': ''}), validators=[allow_only_images_validators])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class': ''}), validators=[allow_only_images_validators])

    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_photo', 'address', 'city', 'state', 'country','pin_code', 'latitude', 'longitude' ]

    def __init__(self, *args, **kwargs):
        super( UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['profile_picture'].widget.attrs['placeholder'] = ''
        self.fields['cover_photo'].widget.attrs['placeholder'] = ''
        self.fields['address'].widget.attrs['placeholder'] = ''
        self.fields['city'].widget.attrs['placeholder'] = ''
        self.fields['state'].widget.attrs['placeholder'] = ''
        self.fields['country'].widget.attrs['placeholder'] = ''
        self.fields['pin_code'].widget.attrs['placeholder'] = ''
        self.fields['latitude'].widget.attrs['placeholder'] = ''
        self.fields['longitude'].widget.attrs['placeholder'] = ''
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            if field == 'latitude' or field == 'longitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'
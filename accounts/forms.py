from django import forms
from . models import User


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
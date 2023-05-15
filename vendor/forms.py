from django import forms

from .models import Vendor
from accounts.validators import allow_only_images_validators


class VendorForm(forms.ModelForm):
    vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class': ''}), validators=[allow_only_images_validators])
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']
    
    def __init__(self, *args, **kwargs):
        super(VendorForm, self).__init__(*args, **kwargs)
        self.fields['vendor_name'].widget.attrs['placeholder'] = ''
        self.fields['vendor_license'].widget.attrs['placeholder'] = ''
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
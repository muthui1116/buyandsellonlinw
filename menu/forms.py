from django import forms
from .models import Category, OnlineItem


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']

    def __init__(self, *args, **kwargs):
        super( CategoryForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class OnlineItemForm(forms.ModelForm):
    class Meta:
        model = OnlineItem
        fields = ['category', 'item_title', 'description', 'price', 'image', 'is_available']

    def __init__(self, *args, **kwargs):
        super( OnlineItemForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            if field == 'is_available':
                self.fields[field].widget.attrs['class'] = 'form-check-input'
                self.fields[field].widget.attrs['type'] = 'checkbox'
                

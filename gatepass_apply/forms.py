from django import forms
from gatepass_apply.models import Gatepass


class ApplyForm(forms.ModelForm):
    class Meta():
        model = Gatepass
        fields = ('from_date', 'to_date', 'purpose', 'address_during_leave', 'applied_on',)
        widgets = {
            'from_date': forms.TextInput(
                attrs={'class': 'form-control datetimepicker-input', 'data-target': '#datetimepicker1'}),
            'applied_on': forms.TextInput(attrs={'class': 'form-control', }),
            'to_date': forms.TextInput(
                attrs={'class': 'form-control datetimepicker-input', 'data-target': '#datetimepicker2'}),
            'purpose': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'address_during_leave': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
        }

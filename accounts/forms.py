from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from accounts.models import Profile


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


user_category = (
    ('BH1 Supervisor', 'BH1 Supervisor'),
    ('BH2 Supervisor', 'BH2 Supervisor'),
    ('BH3 Supervisor', 'BH3 Supervisor'),
    ('GH Supervisor', 'GH Supervisor'),
    ('Control Room', 'Control Room'),
    ('Student', 'Student'),
)


class ProfileUpdateForm(forms.ModelForm):
    class Meta():
        model = Profile
        exclude = ('user', 'user_type',)
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}),
            'roll_no': forms.TextInput(attrs={'placeholder': 'Roll number', 'class': 'form-control'}),
            'mob_no': forms.TextInput(attrs={'placeholder': 'Mobile number', 'class': 'form-control'}),
            'email_id': forms.TextInput(attrs={'placeholder': 'Email-ID', 'class': 'form-control'}),
            'room_no': forms.TextInput(attrs={'placeholder': 'Room number', 'class': 'form-control'}),
            'father_name': forms.TextInput(attrs={'placeholder': 'Father\'s name', 'class': 'form-control'}),
            'father_mobile': forms.TextInput(attrs={'placeholder': 'Father\'s mobile number', 'class': 'form-control'}),
            'hostel': forms.Select(attrs={'class': 'form-control'}),
        }

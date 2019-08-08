from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from accounts.models import Profile


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


hostel_choice = (
    ('BH1', 'BH1'),
    ('BH2', 'BH2'),
    ('BH3', 'BH3'),
    ('GH', 'GH'),
)

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
        exclude = ('roll_no', 'room_no', 'hostel')
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
            'user_type': forms.Select(attrs={'class': 'form-control'}),
            'user': forms.TextInput(attrs={'placeholder': 'User', 'class': 'form-control'}),
        }

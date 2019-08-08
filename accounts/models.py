from django.db import models
from django.contrib.auth.models import User

# Create your models here.

hostel_choice = (
    ('BH1(Arawali Hostel)', 'BH1(Arawali Hostel)'),
    ('BH2(Nilgiri Hostel)', 'BH2(Nilgiri Hostel)'),
    ('BH3(Shivalik Hostel)', 'BH3(Shivalik Hostel)'),
    ('GH(Gangotri Hostel)', 'GH(Gangotri Hostel)'),
)

user_category = (
    ('BH1 Supervisor', 'BH1 Supervisor'),
    ('BH1 Warden', 'BH1 Warden'),
    ('BH1 Assistant Warden', 'BH1 Assistant Warden'),

    ('BH2 Supervisor', 'BH2 Supervisor'),
    ('BH2 Warden', 'BH2 Warden'),
    ('BH2 Assistant Warden', 'BH2 Assistant Warden'),

    ('BH3 Supervisor', 'BH3 Supervisor'),
    ('BH3 Warden', 'BH3 Warden'),
    ('BH3 Assistant Warden', 'BH3 Assistant Warden'),

    ('GH Supervisor', 'GH Supervisor'),
    ('GH Warden', 'GH Warden'),
    ('GH Assistant Warden', 'GH Assistant Warden'),

    ('Control Room', 'Control Room'),
    ('Student', 'Student'),
    ('Admin', 'Admin'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    roll_no = models.CharField(max_length=20, null=True, blank=True)
    mob_no = models.CharField(max_length=11, null=True, blank=True)
    email_id = models.CharField(max_length=30, null=True, blank=True)
    room_no = models.CharField(max_length=3, null=True, blank=True)
    father_name = models.CharField(max_length=50, null=True, blank=True)
    father_mobile = models.CharField(max_length=11, null=True, blank=True)
    hostel = models.CharField(max_length=30, choices=hostel_choice, default='BH1(Arawali Hostel)')
    pic = models.ImageField(upload_to='accounts/pics', null=True, blank=True)
    user_type = models.CharField(max_length=30, choices=user_category, default='Student')

    def __str__(self):
        return self.user.username + '\'s profile'

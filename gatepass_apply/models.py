from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.

status_choice = (
    ('Pending', "Pending"),
    ('Approved', "Approved"),
    ('Rejected', "Rejected"),
)


class Gatepass(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    roll_no = models.CharField(max_length=20, null=True, blank=True)
    mob_no = models.CharField(max_length=11, null=True, blank=True)
    room_no = models.CharField(max_length=3, null=True, blank=True)
    father_name = models.CharField(max_length=50, null=True, blank=True)
    father_mobile = models.CharField(max_length=11, null=True, blank=True)
    hostel = models.CharField(max_length=5)
    pic = models.ImageField(upload_to='gatepass_apply/pics', null=True, blank=True)

    applied_on = models.DateTimeField(default=datetime.now, blank=True)
    from_date = models.CharField(default="", max_length=30)
    to_date = models.CharField(default="", max_length=30)
    purpose = models.CharField(max_length=500)
    address_during_leave = models.CharField(max_length=100)
    hostel_supervisor = models.CharField(max_length=20, choices=status_choice, default="Pending")
    hostel_supervisor_remark = models.CharField(max_length=500, default="N/A")
    hostel_warden = models.CharField(max_length=20, choices=status_choice, default="Pending")
    hostel_warden_remark = models.CharField(max_length=500, default="N/A")
    hostel_assistant_warden = models.CharField(max_length=20, choices=status_choice, default="Pending")
    hostel_assistant_warden_remark = models.CharField(max_length=500, default="N/A")
    control_room = models.CharField(max_length=20, choices=status_choice, default="Pending")
    control_room_remark = models.CharField(max_length=500, default="N/A")

    def __str__(self):
        return str(self.id)


class Item(models.Model):
    gatepass = models.ForeignKey(Gatepass, on_delete=models.CASCADE)
    detail = models.CharField(max_length=500)
    quantity = models.CharField(max_length=3)
    remark = models.CharField(max_length=500)

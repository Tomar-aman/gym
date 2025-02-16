from django.db import models
from users.models import Address
from gym_management.models import Gym , GymPlan 

class GymMembersByOwner(models.Model):
  id = models.AutoField(primary_key=True)
  gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='owner_members')
  name = models.CharField(max_length=255)
  email = models.EmailField(null=True, blank=True)
  phone_number = models.CharField(max_length=15,unique=True)
  gender = models.CharField(max_length=10)
  address = models.OneToOneField(Address, on_delete=models.CASCADE)
  dob = models.DateField(null=True, blank=True)
  photo = models.ImageField(upload_to='members/photos/',null=True, blank=True)
  documents = models.FileField(upload_to='members/documents/',null=True, blank=True) 
  weight = models.FloatField(null=True, blank=True)
  height = models.FloatField(null=True, blank=True)
  is_delete = models.BooleanField(default=False)
  is_archive = models.BooleanField(default=False)
  joined_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name

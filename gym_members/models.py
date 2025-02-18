from django.db import models
from users.models import Address , User
from gym_management.models import Gym , GymPlan 
import uuid

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

class GymMembersByGymCode(models.Model):
  id = models.CharField(max_length=20, primary_key=True, unique=True)
  gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='code_members')
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gym_codes')
  is_archive = models.BooleanField(default=False)
  is_delete = models.BooleanField(default=False)
  joined_at = models.DateTimeField(auto_now_add=True)

  def save(self, *args, **kwargs):
        if not self.id:
            self.id = f"CUSTOM-{uuid.uuid4().hex[:8]}"  # Example format
        super().save(*args, **kwargs)

  def __str__(self):
    return self.user.full_name
  

class UserGymPlan(models.Model):
    id = models.AutoField(primary_key=True)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='gym_memberships')
    gym_plan = models.ForeignKey(GymPlan, on_delete=models.CASCADE, related_name='subscribed_users')
    # Store either an Offline Member OR an Online User
    offline_member = models.ForeignKey(GymMembersByOwner, on_delete=models.CASCADE, null=True, blank=True, related_name="offline_memberships")
    online_member = models.ForeignKey(GymMembersByGymCode, on_delete=models.CASCADE, null=True, blank=True, related_name="online_memberships")

    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()

    def save(self, *args, **kwargs):
        from datetime import timedelta
        
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.gym_plan.duration)  # Auto-set end date

        # Ensure only one type of member is assigned
        if self.offline_member and self.online_member:
            raise ValueError("A gym plan can only be assigned to either an offline or online member, not both.")
        
        super().save(*args, **kwargs)

    def __str__(self):
        member_name = self.offline_member.name if self.offline_member else self.online_member.user.full_name
        return f"{member_name} - {self.gym_plan.name}"

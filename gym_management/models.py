from django.db import models
from users.models import User, Address



class Gym(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gyms', limit_choices_to={'role': 'owner'})
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class GymImage(models.Model):
    image = models.ImageField(upload_to='gyms/photos/')
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='gym_images')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class GymPlan(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='plans')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in days",null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.gym.name}"


class GymProduct(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.gym.name}"
    
class ProductImage(models.Model):
    image = models.ImageField(upload_to='product/photos/')
    gym = models.ForeignKey(GymProduct, on_delete=models.CASCADE, related_name='product_images')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
class GymMember(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gym_memberships')
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='members')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='inactive')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'gym')  # Prevent duplicate memberships

    def __str__(self):
        return f"{self.user.full_name} - {self.gym.name}"

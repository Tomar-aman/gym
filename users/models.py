from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta
from django.utils.timezone import now
from .manager import UserManager
import random

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.country} - {self.postal_code}"

class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    full_name = models.CharField(max_length=72,null=True, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)  # In kilograms
    height = models.FloatField(null=True, blank=True)  # In centimeters
    dob = models.DateField(null=True, blank=True)  # Date of Birth
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True)
    role = models.CharField(
        max_length=15,
        choices=[('user', 'User'), ('owner', 'Owner')],
        default='user'
    )
    is_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'  # Use email for authentication
    REQUIRED_FIELDS = []

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="documents")
    document = models.FileField(upload_to='user_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document {self.id} for {self.user.username}"

class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_otp_expired(self):
        return now() < (self.created_at + timedelta(minutes=10))

    def generate_otp(self):
        self.otp_code = f"{random.randint(100000, 999999)}"
        self.save()

from rest_framework import serializers
from .models import User,OTP
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .utils import send_otp_email

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'full_name', 'password', 'role']

    def create(self, validated_data):
        # Use the `create_user` method from your custom user manager
        user = User.objects.create_user(
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            full_name=validated_data.get('full_name'),
            role=validated_data.get('role', 'user'),
            password=validated_data['password']
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)  # Email or Phone number
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Validate credentials
        user = User.objects.filter(email=email).first() #or User.objects.filter(phone_number=identifier).first()
        if not user:
            raise serializers.ValidationError("Invalid credentials.")

        # Authenticate user
        authenticated_user = authenticate(email=user.email, password=password)
        if not authenticated_user:
            raise serializers.ValidationError("Invalid credentials.")

        # Add user object to validated data
        data['user'] = user
        return data

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }

class SendOTPSerializer(serializers.Serializer):
    def save(self, user):
        # Save OTP to database
        otp, created = OTP.objects.get_or_create(user=user)
        otp.generate_otp()
        # Send OTP email
        send_otp_email(user, otp.otp_code)


class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(required=True)

    def validate_otp(self, value):
        # Validate OTP exists
        otp = OTP.objects.filter(otp_code=value).first()
        if not otp:
            raise serializers.ValidationError("Invalid OTP.")
        if otp.is_otp_expired:
            raise serializers.ValidationError("OTP has expired. Please request a new one.")
        return otp

    def save(self, otp):
        # Mark user as verified
        user = otp.user
        user.is_verified = True
        user.save()

        # Delete the OTP after verification
        otp.delete()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'full_name', 'weight', 'height', 'dob', 'role', 'is_verified', 'photo','address']

    # Optionally, you can add custom fields like the address:
    address = serializers.SerializerMethodField()

    def get_address(self, obj):
        return obj.address.street if obj.address else None
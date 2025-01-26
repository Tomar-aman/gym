from rest_framework import serializers
from .models import Gym, GymImage, GymPlan, GymProduct, ProductImage, GymMember
from users.serializers import AddressSerializer 
from users.models import Address

class GymImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymImage
        fields = ['id', 'image', 'uploaded_at', 'gym']  # Include 'gym' in fields

    def create(self, validated_data):
        # Ensure the gym is correctly assigned
        return GymImage.objects.create(**validated_data)


class GymPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymPlan
        fields = ['id', 'name', 'price', 'description', 'gym']

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value


class GymProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymProduct
        fields = ['id', 'name', 'price', 'description', 'gym']

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'uploaded_at', 'gym_product']


class GymMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymMember
        fields = ['id', 'user', 'gym', 'status', 'joined_at']
        read_only_fields = ['joined_at']


class GymSerializer(serializers.ModelSerializer):
    gym_images = GymImageSerializer(many=True, read_only=True)
    plans = GymPlanSerializer(many=True, read_only=True)
    products = GymProductSerializer(many=True, read_only=True)
    members = GymMemberSerializer(many=True, read_only=True)
    address = AddressSerializer()  # Nested serializer for address

    class Meta:
        model = Gym
        fields = ['id', 'name', 'owner', 'address', 'status', 'gym_images', 'plans', 'products', 'members']
        read_only_fields = ['status', 'owner']

    def create(self, validated_data):
        address_data = validated_data.pop('address')  # Extract address data
        address = Address.objects.create(**address_data)  # Create a new Address object
        validated_data['owner'] = self.context['request'].user  # Set the owner to the current user
        gym = Gym.objects.create(address=address, **validated_data)  # Create the Gym object
        return gym
from rest_framework import serializers
from .models import GymMembersByOwner ,UserGymPlan
from users.serializers import AddressSerializer , Address

class GymMemberSerializer(serializers.ModelSerializer):
    address = AddressSerializer()  # Nested serializer
    class Meta:
        model = GymMembersByOwner
        fields = '__all__'

    def create(self, validated_data):
        """Create a GymMember with a nested Address"""
        address_data = validated_data.pop('address')
        address = Address.objects.create(**address_data)  # Create address instance
        member = GymMembersByOwner.objects.create(address=address, **validated_data)  # Create member
        return member

    def update(self, instance, validated_data):
        """Update GymMember and Address"""
        address_data = validated_data.pop('address', None)
        if address_data:
            for attr, value in address_data.items():
                setattr(instance.address, attr, value)  # Update address fields
            instance.address.save()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)  # Update member fields
        instance.save()
        return instance
    
class UserGymPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGymPlan
        fields = '__all__'

    def validate(self, data):
        if not data.get("offline_member") and not data.get("online_member"):
            raise serializers.ValidationError("You must assign the plan to either an offline or online member.")
        if data.get("offline_member") and data.get("online_member"):
            raise serializers.ValidationError("A gym plan can only be assigned to either an offline or online member, not both.")
        return data

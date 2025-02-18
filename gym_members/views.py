from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import GymMembersByOwner, GymMembersByGymCode, UserGymPlan , GymPlan
from rest_framework.generics import ListCreateAPIView
from .serializers import GymMemberSerializer, UserGymPlanSerializer
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from datetime import timedelta
class GymMemberAPI(APIView):

    def get(self, request, pk=None):
        gym_id = request.query_params.get('gym_id')
        is_archive = request.query_params.get('is_archive') or False
        if pk:
            try:
              member = GymMembersByOwner.objects.get(pk=pk, is_delete=False)
            except GymMembersByOwner.DoesNotExist:
                return Response({"error": "Gym member not found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = GymMemberSerializer(member)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        members = GymMembersByOwner.objects.filter(is_delete=False,gym__id=gym_id, is_archive=is_archive)
        serializer = GymMemberSerializer(members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = GymMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            member = get_object_or_404(GymMembersByOwner, pk=pk)
        except GymMembersByOwner.DoesNotExist:
            return Response({"error": "Gym member not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = GymMemberSerializer(member, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            member = get_object_or_404(GymMembersByOwner, pk=pk)
        except GymMembersByOwner.DoesNotExist:
            return Response({"error": "Gym member not found."}, status=status.HTTP_404_NOT_FOUND)
        
        member.is_delete = True
        member.phone_number += "_del"
        member.email += "_deleted"
        member.save()
        return Response({"message": "Gym member deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
class AssignGymPlanView(ListCreateAPIView):
    queryset = UserGymPlan.objects.all()
    serializer_class = UserGymPlanSerializer

    def get(self,request):
        gym_id = request.query_params.get('gym_id')
        active_user = UserGymPlan.objects.filter(gym__id=gym_id)
        serilaizer =  self.serializer_class(active_user, many=True)
        return Response(serilaizer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        gym_id = request.data.get('gym')
        gym_plan_id = request.data.get('gym_plan')
        user_id = request.data.get('user')  # Single user ID

        if not user_id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not gym_id or not gym_plan_id:
              return Response({"error": "Gym and Gym Plan are required."}, status=status.HTTP_400_BAD_REQUEST)

          # Check if the GymPlan exists
        gym_plan = GymPlan.objects.filter(id=gym_plan_id, gym_id=gym_id).first()
        if not gym_plan:
            return Response({"error": "Gym Plan not found."}, status=status.HTTP_404_NOT_FOUND)
        # Check if the user exists in either offline or online members
        offline_member = GymMembersByOwner.objects.filter(id=user_id, gym_id=gym_id).first()
        online_member = GymMembersByGymCode.objects.filter(id=user_id, gym_id=gym_id).first()

        if not offline_member and not online_member:
            return Response({"error": "User not found or does not belong to this gym."},
                            status=status.HTTP_404_NOT_FOUND)
        start_date = now().date()
        end_date = start_date + timedelta(days=gym_plan.duration)
        # Create UserGymPlan record
        gym_plan_data = {
            "gym": gym_id,
            "gym_plan": gym_plan_id,
            "offline_member": offline_member.id if offline_member else None,
            "online_member": online_member.id if online_member else None,
            "start_date": start_date,
            "end_date": end_date
        }

        serializer = self.get_serializer(data=gym_plan_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Gym plan assigned successfully.", "data": serializer.data},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
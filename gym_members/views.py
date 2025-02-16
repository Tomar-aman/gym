from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .models import GymMembersByOwner
from .serializers import GymMemberSerializer
from django.shortcuts import get_object_or_404

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
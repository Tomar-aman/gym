from django.db import transaction
from rest_framework import status , serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Gym, GymPlan, GymProduct, GymMember
from .serializers import (
    GymSerializer,
    GymPlanSerializer,
    GymProductSerializer,
    GymMemberSerializer,
    GymImageSerializer
)


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class GymListCreateAPI(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request):
        gyms = Gym.objects.filter(owner=request.user)
        serializer = GymSerializer(gyms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if Gym.objects.filter(owner=request.user).exists():
            return Response(
                {"error": "You can only create one gym."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = GymSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GymImageUploadAPI(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, gym_id):
        try:
            gym = Gym.objects.get(id=gym_id, owner=request.user)
        except Gym.DoesNotExist:
            return Response({"error": "Gym not found or you do not have permission."}, status=status.HTTP_404_NOT_FOUND)

        images = request.FILES.getlist('images')
        if not images:
            return Response({"error": "No images provided."}, status=status.HTTP_400_BAD_REQUEST)

        image_data = [{'image': image, 'gym': gym.id} for image in images]
        serializer = GymImageSerializer(data=image_data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GymDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Gym.objects.get(pk=pk, owner=user)
        except Gym.DoesNotExist:
            return None

    def get(self, request, pk):
        gym = self.get_object(pk, request.user)
        if gym:
            serializer = GymSerializer(gym)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Gym not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        gym = self.get_object(pk, request.user)
        if gym:
            serializer = GymSerializer(gym, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Gym not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        gym = self.get_object(pk, request.user)
        if gym:
            gym.delete()
            return Response({"message": "Gym deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Gym not found."}, status=status.HTTP_404_NOT_FOUND)


class GymPlanAPI(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def post(self, request):
        serializer = GymPlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        gym_id = request.query_params.get('gym_id')
        print(gym_id)
        if gym_id:
            plans = GymPlan.objects.filter(gym__owner=request.user)

            if gym_id:
                plans = plans.filter(gym_id=gym_id)

            serializer = GymPlanSerializer(plans, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class GymProductAPI(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def post(self, request):
        serializer = GymProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        products = GymProduct.objects.filter(gym__owner=request.user)
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(products, request)
        serializer = GymProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class GymMemberAPI(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def post(self, request):
        serializer = GymMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        memberships = GymMember.objects.filter(gym__owner=request.user)
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(memberships, request)
        serializer = GymMemberSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
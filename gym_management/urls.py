from django.urls import path
from .views import (
    GymListCreateAPI,
    GymImageUploadAPI,
    GymDetailAPI,
    GymPlanAPI,
    GymProductAPI,
    GymMemberAPI,
)

urlpatterns = [
    path('gyms/', GymListCreateAPI.as_view(), name='gym_list_create'),
     path('<int:gym_id>/upload-image/', GymImageUploadAPI.as_view(), name='gym_upload_image'),
    path('gyms/<int:pk>/', GymDetailAPI.as_view(), name='gym_detail'),
    path('plans/', GymPlanAPI.as_view(), name='gym_plans'),
    path('products/', GymProductAPI.as_view(), name='gym_products'),
    path('memberships/', GymMemberAPI.as_view(), name='gym_memberships'),
]



from django.urls import path
from .views import GymMemberAPI , AssignGymPlanView

urlpatterns = [
    path('members/', GymMemberAPI.as_view(), name='gym_memberships'),
    path('members/<int:pk>/', GymMemberAPI.as_view(), name='member'),
    path('assign-plan/', AssignGymPlanView.as_view(), name='assign_plan'),
]
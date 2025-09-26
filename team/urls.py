from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api

router = DefaultRouter()
router.register(r'members', api.TeamMemberViewSet, basename='team-members')
router.register(r'departments', api.DepartmentViewSet)

urlpatterns = [
    path('api/team/', include(router.urls)),
    path('api/team/stats/', api.team_stats, name='team-stats'),
]
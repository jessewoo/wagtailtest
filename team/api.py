from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import TeamMember, Department
from .serializers import TeamMemberSerializer, DepartmentSerializer


class TeamMemberPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 50


class TeamMemberViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for team members
    Supports filtering, searching, and ordering
    """
    serializer_class = TeamMemberSerializer
    pagination_class = TeamMemberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['department', 'is_active', 'is_featured']
    search_fields = ['name', 'job_title', 'bio', 'specialties']
    ordering_fields = ['name', 'job_title', 'sort_order', 'start_date']
    ordering = ['sort_order', 'name']
    
    def get_queryset(self):
        return TeamMember.objects.select_related('department').prefetch_related('social_links')


class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for departments
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


@api_view(['GET'])
def team_stats(request):
    """Custom endpoint for team statistics"""
    stats = {
        'total_members': TeamMember.objects.count(),
        'active_members': TeamMember.objects.filter(is_active=True).count(),
        'featured_members': TeamMember.objects.filter(is_featured=True).count(),
        'departments': Department.objects.count(),
        'departments_with_members': Department.objects.filter(team_members__isnull=False).distinct().count()
    }
    return Response(stats)
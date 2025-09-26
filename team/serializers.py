from rest_framework import serializers
from wagtail.images.api.fields import ImageRenditionField
from .models import TeamMember, Department, TeamMemberSocialLink


class SocialLinkSerializer(serializers.ModelSerializer):
    platform_display = serializers.CharField(source='get_platform_display', read_only=True)
    
    class Meta:
        model = TeamMemberSocialLink
        fields = ['platform', 'platform_display', 'url']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description']


class TeamMemberSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    social_links = SocialLinkSerializer(many=True, read_only=True)
    specialty_list = serializers.ReadOnlyField()
    
    # Image renditions for different sizes
    photo_thumbnail = ImageRenditionField('fill-150x150', source='photo')
    photo_medium = ImageRenditionField('fill-300x300', source='photo')
    photo_large = ImageRenditionField('fill-500x500', source='photo')
    
    class Meta:
        model = TeamMember
        fields = [
            'id', 'name', 'job_title', 'department', 'email', 'phone',
            'photo_thumbnail', 'photo_medium', 'photo_large',
            'bio', 'short_bio', 'years_experience', 'specialties', 'specialty_list',
            'is_active', 'is_featured', 'sort_order', 'start_date',
            'social_links', 'created_at', 'updated_at'
        ]
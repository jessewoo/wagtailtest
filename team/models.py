from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.api import APIField
from wagtail.images.api.fields import ImageRenditionField
from wagtail.snippets.models import register_snippet
from wagtail.search import index
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from rest_framework import serializers


# Department snippet for organizing team members
@register_snippet
class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    panels = [
        FieldPanel('name'),
        FieldPanel('description'),
    ]
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


# Social media links for team members
class TeamMemberSocialLink(models.Model):
    team_member = ParentalKey(
        'TeamMember',
        related_name='social_links',
        on_delete=models.CASCADE
    )
    
    SOCIAL_CHOICES = [
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter'),
        ('github', 'GitHub'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('website', 'Personal Website'),
        ('email', 'Email'),
    ]
    
    platform = models.CharField(max_length=20, choices=SOCIAL_CHOICES)
    url = models.URLField()
    
    panels = [
        FieldPanel('platform'),
        FieldPanel('url'),
    ]
    
    def __str__(self):
        return f"{self.team_member.name} - {self.get_platform_display()}"


# Team Member snippet model
@register_snippet
class TeamMember(index.Indexed, ClusterableModel):
    # Basic information
    name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='team_members'
    )
    
    # Contact information
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    # Profile information
    photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    bio = RichTextField(blank=True)
    short_bio = models.TextField(
        max_length=500,
        blank=True,
        help_text="Brief description for listings"
    )
    
    # Professional details
    years_experience = models.PositiveIntegerField(null=True, blank=True)
    specialties = models.TextField(
        blank=True,
        help_text="Comma-separated list of specialties"
    )
    
    # Status and ordering
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)
    
    # Timestamps
    start_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    panels = [
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('job_title'),
            FieldPanel('department'),
        ], heading="Basic Information"),
        
        MultiFieldPanel([
            FieldPanel('email'),
            FieldPanel('phone'),
        ], heading="Contact Information"),
        
        MultiFieldPanel([
            FieldPanel('photo'),
            FieldPanel('short_bio'),
            FieldPanel('bio'),
        ], heading="Profile"),
        
        MultiFieldPanel([
            FieldPanel('years_experience'),
            FieldPanel('specialties'),
            FieldPanel('start_date'),
        ], heading="Professional Details"),
        
        MultiFieldPanel([
            FieldPanel('is_active'),
            FieldPanel('is_featured'),
            FieldPanel('sort_order'),
        ], heading="Status & Display"),
        
        InlinePanel('social_links', label="Social Media Links"),
    ]
    
    search_fields = [
        index.SearchField('name'),
        index.SearchField('job_title'),
        index.SearchField('bio'),
        index.SearchField('specialties'),
    ]
    
    def __str__(self):
        return f"{self.name} - {self.job_title}"
    
    @property
    def specialty_list(self):
        """Return specialties as a list"""
        if self.specialties:
            return [s.strip() for s in self.specialties.split(',')]
        return []
    
    class Meta:
        ordering = ['sort_order', 'name']


# Team page model to display team members
class TeamPage(Page):
    intro = RichTextField(blank=True)
    show_departments = models.BooleanField(
        default=True,
        help_text="Group team members by department"
    )
    show_only_active = models.BooleanField(
        default=True,
        help_text="Only show active team members"
    )
    show_only_featured = models.BooleanField(
        default=False,
        help_text="Only show featured team members"
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        MultiFieldPanel([
            FieldPanel('show_departments'),
            FieldPanel('show_only_active'),
            FieldPanel('show_only_featured'),
        ], heading="Display Options"),
    ]
    
    def get_team_members(self):
        """Get filtered team members"""
        team_members = TeamMember.objects.all()
        
        if self.show_only_active:
            team_members = team_members.filter(is_active=True)
        
        if self.show_only_featured:
            team_members = team_members.filter(is_featured=True)
        
        return team_members.order_by('sort_order', 'name')
    
    def get_departments_with_members(self):
        """Get departments with their team members"""
        departments = Department.objects.prefetch_related('team_members').all()
        result = []
        
        for dept in departments:
            members = dept.team_members.all()
            if self.show_only_active:
                members = members.filter(is_active=True)
            if self.show_only_featured:
                members = members.filter(is_featured=True)
            
            if members.exists():
                result.append({
                    'department': dept,
                    'members': members.order_by('sort_order', 'name')
                })
        
        return result
    
    # API fields
    api_fields = [
        APIField('intro'),
        APIField('show_departments'),
        APIField('team_members', serializer=serializers.SerializerMethodField()),
    ]
    
    def get_team_members_for_api(self, obj):
        """Custom serializer method for API"""
        team_members = obj.get_team_members()
        return TeamMemberSerializer(team_members, many=True, context={'request': self.context.get('request')}).data

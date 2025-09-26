from django.core.management.base import BaseCommand
from team.models import Department, TeamMember
from wagtail.images.models import Image

class Command(BaseCommand):
    help = 'Create sample team data'
    
    def handle(self, *args, **options):
        # Create departments
        engineering = Department.objects.get_or_create(
            name="Engineering",
            defaults={'description': "Our technical team building amazing products"}
        )[0]
        
        marketing = Department.objects.get_or_create(
            name="Marketing",
            defaults={'description': "Spreading the word about our awesome work"}
        )[0]
        
        design = Department.objects.get_or_create(
            name="Design",
            defaults={'description': "Creating beautiful user experiences"}
        )[0]
        
        # Create sample team members
        team_data = [
            {
                'name': 'John Smith',
                'job_title': 'Senior Software Engineer',
                'department': engineering,
                'email': 'john@example.com',
                'short_bio': 'Full-stack developer with 8 years of experience in Python and JavaScript.',
                'years_experience': 8,
                'specialties': 'Python, Django, React, PostgreSQL',
                'is_featured': True,
            },
            {
                'name': 'Sarah Johnson',
                'job_title': 'Marketing Manager',
                'department': marketing,
                'email': 'sarah@example.com',
                'short_bio': 'Digital marketing expert specializing in content strategy and SEO.',
                'years_experience': 6,
                'specialties': 'SEO, Content Marketing, Social Media',
                'is_featured': True,
            },
            {
                'name': 'Mike Chen',
                'job_title': 'UX Designer',
                'department': design,
                'email': 'mike@example.com',
                'short_bio': 'User experience designer passionate about creating intuitive interfaces.',
                'years_experience': 5,
                'specialties': 'UI/UX Design, Figma, User Research',
            },
        ]
        
        for data in team_data:
            member, created = TeamMember.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                self.stdout.write(f'Created team member: {member.name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample team data')
        )
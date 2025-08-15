from django.core.management.base import BaseCommand
from accounts.models import Organization, User

class Command(BaseCommand):
    help = 'Create superuser with organization'

    def handle(self, *args, **options):
        org = Organization.objects.get_or_create(name="Admin Organization")[0]
        User.objects.create_superuser(
            username="admin123",
            email="admin@example.com",
            password="Secure@Password123",  # Change this!
            organization=org,
            role="ADMIN"
        )
        self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from base.models import UserProfile

class Command(BaseCommand):
    help = 'Create missing user profiles for existing users'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        created = 0
        for user in users:
            if not hasattr(user, 'userprofile'):
                UserProfile.objects.create(user=user)
                created += 1
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created} UserProfiles'))
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create a test user with superuser privileges'

    def handle(self, *args, **options):
        username = 'testuser'
        password = 'testpassword'
        email = 'testuser@example.com'
        if not get_user_model().objects.filter(username=username).exists():
            get_user_model().objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS('Successfully created superuser with username "{}" and password "{}".'.format(username, password)))
        else:
            self.stdout.write(self.style.WARNING('User "{}" already exists. Please choose a different username.'.format(username)))

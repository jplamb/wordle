from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

class Command(BaseCommand):
    help = 'Create a random application token'

    def handle(self, *args, **kwargs):
        token = get_random_string(length=64)
        self.stdout.write(self.style.SUCCESS('Generated application token:'))
        self.stdout.write(token)

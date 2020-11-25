from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create User"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str, help="The username to be registered")
        parser.add_argument("password", type=str, help="The password of the user")

    def handle(self, username, password, *args, **kwargs):
        User.objects.create_user(username=username, password=password)

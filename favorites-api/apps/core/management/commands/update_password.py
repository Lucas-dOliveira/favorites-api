from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Update user password"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str, help="The username of the user")
        parser.add_argument("password", type=str, help="New password")

    def handle(self, username, password, *args, **kwargs):
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()

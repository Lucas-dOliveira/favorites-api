import pytest
from django.contrib.auth.models import User
from django.core.management import call_command

pytestmark = pytest.mark.django_db


def test_create_user():
    new_user = {"username": "random-service", "password": "W]3`sn.Pb]SJ.vE@@`KPB/?xj:y<GR^;"}

    call_command("create_user", *new_user.values())

    user = User.objects.get(username=new_user["username"])
    assert user.check_password(new_user["password"])


def test_update_password(user):
    new_password = "super-secret-123-password"

    call_command("update_password", user.username, new_password)

    user.refresh_from_db()
    assert user.check_password(new_password)

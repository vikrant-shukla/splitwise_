import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

data = [
    {
        "email": "user1@gmail.com",
        "phone_number": "76478293",
        "first_name": "vik",
        "last_name": "vik",
    },
    {
        "email": "user2@gmail.com",
        "phone_number": "",
        "first_name": "lcy",
        "last_name": "lcy",
    },
    {
        "email": "user3@gmail.com",
        "phone_number": "",
        "first_name": "xyz",
        "last_name": "xyz",
    },
    {
        "email": "user4@gmail.com",
        "phone_number": "",
        "first_name": "abc",
        "last_name": "abc",
    },
]


class Command(BaseCommand):
    """
    overview: creation of all users using this class Command.
    """

    def handle(self, *args, **options):
        [
            User.objects.create_user(
                first_name=i["first_name"],
                username=f"@{random.randint(1,100)}",
                last_name=i["last_name"],
                email=i["email"],
                password=f"pass@{1233}",
            )
            for i in data
        ]
        self.stdout.write(self.style.SUCCESS(f"User created"))

import logging

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        logger = logging.getLogger("django")

        queryset = get_user_model().objects.all()

        logger.info(f"Current amount of users before: {queryset.count()}")

        # check user name admin
        # @DJANGO_SUPERUSER_PASSWORD=admin123 admin admin@gmail.com
        base_name = "admin"
        base_email = "admin@gmail.com"
        base_password = "admin123"
        if not queryset.filter(username=base_name).exists():
            get_user_model().objects.create_superuser(
                username=base_name,
                email=base_email,
                password=base_password,
            )
            logger.info(f"Create new users Name: {base_name} and (password is {base_password})")
        else:
            logger.info(f"User Name: {base_name} already exists")

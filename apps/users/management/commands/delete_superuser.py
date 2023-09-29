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

        base_name = "admin"
        if not queryset.filter(username=base_name).exists():
            logger.info(f"User Name: {base_name} does not exist")
        else:
            total_deleted, details = queryset.all().filter(username=base_name).delete()
            logger.info(f"User Name: {base_name} was deleted")

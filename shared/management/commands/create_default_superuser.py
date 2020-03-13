import logging
import os

from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.management import BaseCommand
from django.db import IntegrityError

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a default superuser account'

    def handle(self, *args, **options):
        logger = logging.getLogger('django')
        username = settings.DEFAULT_ADMIN_USERNAME
        email = settings.DEFAULT_ADMIN_EMAIL
        password = settings.DEFAULT_ADMIN_PASSWORD

        try:
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
        except IntegrityError as error:
            logger.warning("DB Error Thrown %s" % error)

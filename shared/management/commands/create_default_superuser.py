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
        first_name = settings.DEFAULT_ADMIN_FIRST_NAME
        last_name = settings.DEFAULT_ADMIN_LAST_NAME

        try:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password,
                )
                user.first_name = first_name
                user.last_name = last_name
                user.save()
        except IntegrityError as error:
            logger.warning("DB Error Thrown %s" % error)

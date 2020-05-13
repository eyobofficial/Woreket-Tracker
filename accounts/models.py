from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from shared.constants import ROLE_ADMIN, ROLE_MANAGEMENT, ROLE_STAFF, \
    ROLE_SUPPLIER
from purchases.models import Supplier

from .managers import CustomUserManager


ROLE_GROUPS = [ROLE_ADMIN, ROLE_MANAGEMENT, ROLE_STAFF, ROLE_SUPPLIER]


class CustomUser(AbstractUser):
    PENDING = 1
    ACTIVE = 2
    DISABLED = 3

    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (ACTIVE, 'Active'),
        (DISABLED, 'Disabled')
    )

    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    email = models.EmailField('email address', unique=True)
    phone_number = PhoneNumberField(null=True, unique=True)
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=PENDING
    )
    supplier = models.ForeignKey(
        Supplier,
        null=True, blank=True,
        on_delete=models.SET_NULL,
    )
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    objects = CustomUserManager()

    class Meta(AbstractUser.Meta):
        default_related_name = 'users'

    def __str__(self):
        return self.email

    @property
    def role(self):
        """Gets user role."""
        return self.groups.filter(name__in=ROLE_GROUPS).first()

    @role.setter
    def role(self, role_name):
        """Set user role."""
        try:
            # Predefined roles
            admin_group = Group.objects.get(name=ROLE_ADMIN)
            staff_group = Group.objects.get(name=ROLE_STAFF)
            management_group = Group.objects.get(name=ROLE_MANAGEMENT)
            supplier_group = Group.objects.get(name=ROLE_SUPPLIER)

            # New role
            group = Group.objects.get(name=role_name)
            self.groups.remove(
                admin_group, staff_group, management_group, supplier_group)
            self.groups.add(group)
        except Group.DoesNotExist:
            raise ValueError(f'{role_name} role does not exists.')

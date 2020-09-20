import factory

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from shared.constants import ROLE_ADMIN, ROLE_MANAGEMENT, ROLE_SUPPLIER, \
    ROLE_STAFF, ROLE_GUEST
from purchases.tests.factories import SupplierFactory


User = get_user_model()


class BaseUserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttribute(lambda o: '{}.{}@test.mail'.format(
        o.first_name, o.last_name))

    class Meta:
        model = User


class GroupFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Group


class UserFactory(BaseUserFactory):
    """
    Create a random `User` instance with no role assigned.
    """
    is_staff = False


class SuperuserFactory(BaseUserFactory):
    """
    Create a random `Superuser` instance.
    """
    is_staff = True
    is_superuser = True


class AdminUserFactory(UserFactory):
    """
    Create a random user with `Admin` role.
    """
    @factory.post_generation
    def _attach_role(obj, created, extracted, **kwargs):
        if not created:
            return
        obj.role = ROLE_ADMIN


class ManagementUserFactory(UserFactory):
    """
    Create a random user with `Management` role.
    """
    @factory.post_generation
    def _attach_role(obj, created, extracted, **kwargs):
        if not created:
            return
        obj.role = ROLE_MANAGEMENT


class StaffUserFactory(UserFactory):
    """
    Create a random user with `Staff` role.
    """
    @factory.post_generation
    def _attach_role(obj, created, extracted, **kwargs):
        if not created:
            return
        obj.role = ROLE_STAFF


class GuestUserFactory(UserFactory):
    """
    Create a random user with `Guest` role.
    """
    @factory.post_generation
    def _attach_role(obj, created, extracted, **kwargs):
        if not created:
            return
        obj.role = ROLE_GUEST


class SupplierUserFactory(UserFactory):
    """
    Create a random user with `Supplier` role.
    """
    supplier = factory.SubFactory(SupplierFactory)

    @factory.post_generation
    def _attach_role(obj, created, extracted, **kwargs):
        if not created:
            return
        obj.role = ROLE_SUPPLIER


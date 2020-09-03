from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.tests.factories import UserFactory, AdminUserFactory, \
    GuestUserFactory, ManagementUserFactory, StaffUserFactory

from customers.models import Customer, Union
from .factories import CustomerFactory, UnionFactory


User = get_user_model()


class UnionListViewTests(TestCase):
    """
    Tests for the `UnionListView` test.
    """
    fixtures = ['roles']

    def setUp(self):
        self.template = 'customers/union_list.html'
        self.url = reverse('customers:union-list')
        self.user = UserFactory()
        self.admin = AdminUserFactory()
        self.management = ManagementUserFactory()
        self.staff = StaffUserFactory()
        self.guest = GuestUserFactory()

    def test_request_with_anonymous_user(self):
        """
        Ensure unauthenticated users cannot access the `UnionListView` view.
        """
        response = self.client.get(self.url, follow=True)
        expected_url = f'{reverse("accounts:login")}?next=/customers/unions/'

        # Assertions
        self.assertRedirects(response, expected_url)

    def test_request_with_activated_user_with_admin_role(self):
        """
        Ensure activated users with assigned `ADMIN` role can access
        the `UnionListView` view.
        """
        # Disable user
        self.admin.status = User.ACTIVE
        self.admin.save()

        self.client.force_login(self.admin)
        response = self.client.get(self.url)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

    def test_request_with_activated_user_with_management_role(self):
        """
        Ensure activated users with assigned `MANAGEMENT` role can access
        the `UnionListView` view.
        """
        # Activate user
        self.management.status = User.ACTIVE
        self.management.save()

        self.client.force_login(self.management)
        response = self.client.get(self.url)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

    def test_request_with_activated_user_with_staff_role(self):
        """
        Ensure activated users with assigned `STAFF` role can access
        the `UnionListView` view.
        """
        # Activate user
        self.staff.status = User.ACTIVE
        self.staff.save()

        self.client.force_login(self.staff)
        response = self.client.get(self.url)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

    def test_request_with_activated_user_with_guest_role(self):
        """
        Ensure activated users with assigned `GUEST` role can access
        the `UnionListView` view.
        """
        # Activate user
        self.guest.status = User.ACTIVE
        self.guest.save()

        self.client.force_login(self.guest)
        response = self.client.get(self.url)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

    def test_request_with_disabled_user(self):
        """
        Ensure disabled users cannot access the `UnionListView` view.
        """
        # Disable user
        self.admin.status = User.DISABLED
        self.admin.save()

        self.client.force_login(self.admin)
        response = self.client.get(self.url)

        # Assertions
        self.assertEqual(response.status_code, 403)

    def test_request_with_pending_user(self):
        """
        Ensure users with pending status cannot access the
        `UnionListView` view.
        """
        # Convert user status to pending
        self.admin.status = User.PENDING
        self.admin.save()

        self.client.force_login(self.admin)
        response = self.client.get(self.url)

        # Assertions
        self.assertEqual(response.status_code, 403)


class UnionCreateViewTests(TestCase):
    """
    Tests for the `UnionCreateView` test.
    """
    fixtures = ['roles']

    def setUp(self):
        self.template = 'customers/modals/unions/union_form.html'
        self.url = reverse('customers:union-create')
        self.user = UserFactory()
        self.admin = AdminUserFactory()
        self.management = ManagementUserFactory()
        self.staff = StaffUserFactory()
        self.guest = GuestUserFactory()

    def test_request_with_anonymous_user(self):
        """
        Ensure unauthenticated users cannot access the `UnionCreateView` view.
        """
        response = self.client.get(self.url, follow=True)
        queryparam = '/customers/unions/create/'
        expected_url = f'{reverse("accounts:login")}?next={queryparam}'

        # Assertions
        self.assertRedirects(response, expected_url)

    def test_GET_request_with_activated_user_with_admin_role(self):
        """
        Ensure activated users with assigned `ADMIN` role can access
        the `UnionCreateView` view.
        """
        # Activate user
        self.admin.status = User.ACTIVE
        self.admin.save()

        self.client.force_login(self.admin)
        response = self.client.get(self.url)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

    def test_POST_request_with_activated_user_with_admin_role(self):
        """
        Ensure activated users with assigned `ADMIN` role can send POST
        requests to the `UnionCreateView` view.
        """
        # Activate user
        self.admin.status = User.ACTIVE
        self.admin.save()

        customer = CustomerFactory()
        payload = {
            'name': 'Test union 01',
            'customer': customer.pk
        }

        self.client.force_login(self.admin)
        response = self.client.post(self.url, payload, follow=True)
        expected_url = reverse('customers:union-list')

        # Assertions
        self.assertRedirects(response, expected_url)
        self.assertEqual(Customer.objects.count(), 1)

    def test_GET_request_with_activated_user_with_staff_role(self):
        """
        Ensure activated users with assigned `STAFF` role can access
        the `UnionCreateView` view.
        """
        # Activate user
        self.staff.status = User.ACTIVE
        self.staff.save()

        self.client.force_login(self.staff)
        response = self.client.get(self.url)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

    def test_POST_request_with_activated_user_with_staff_role(self):
        """
        Ensure activated users with assigned `STAFF` role can send POST
        requests to the `UnionCreateView` view.
        """
        # Activate user
        self.staff.status = User.ACTIVE
        self.staff.save()

        customer = CustomerFactory()
        payload = {
            'name': 'Test union 01',
            'customer': customer.pk
        }

        self.client.force_login(self.staff)
        response = self.client.post(self.url, payload, follow=True)
        expected_url = reverse('customers:union-list')

        # Assertions
        self.assertRedirects(response, expected_url)
        self.assertEqual(Union.objects.count(), 1)

    def test_GET_request_with_activated_user_with_management_role(self):
        """
        Ensure activated users with assigned `MANAGEMENT` role cannot access
        the `UnionCreateView` view.
        """
        # Activate user
        self.management.status = User.ACTIVE
        self.management.save()

        self.client.force_login(self.management)
        response = self.client.get(self.url)

        # Assertions
        self.assertEqual(response.status_code, 403)

    def test_GET_request_with_activated_user_with_guest_role(self):
        """
        Ensure activated users with assigned `GUEST` role cannot access
        the `UnionCreateView` view.
        """
        # Activate user
        self.guest.status = User.ACTIVE
        self.guest.save()

        self.client.force_login(self.guest)
        response = self.client.get(self.url)

        # Assertions
        self.assertEqual(response.status_code, 403)

class UnionUpdateViewTests(TestCase):
    """
    Tests for the `UnionUpdateView` test.
    """
    fixtures = ['roles', 'customers']

    def setUp(self):
        self.template = 'customers/modals/unions/union_form.html'
        self.union = UnionFactory()
        self.url = reverse('customers:union-update', args=[self.union.pk])
        self.user = UserFactory()
        self.admin = AdminUserFactory()
        self.management = ManagementUserFactory()
        self.staff = StaffUserFactory()
        self.guest = GuestUserFactory()

    def test_request_with_anonymous_user(self):
        """
        Ensure unauthenticated users cannot access the `UnionUpdateView` view.
        """
        response = self.client.get(self.url, follow=True)
        queryparam = f'/customers/unions/{self.union.pk}/update/'
        expected_url = f'{reverse("accounts:login")}?next={queryparam}'

        # Assertions
        self.assertRedirects(response, expected_url)

    def test_GET_request_with_activated_user_with_admin_role(self):
        """
        Ensure activated users with assigned `ADMIN` role can access
        the `UnionUpdateView` view.
        """
        # Activate user
        self.admin.status = User.ACTIVE
        self.admin.save()

        self.client.force_login(self.admin)
        response = self.client.get(self.url)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

    def test_POST_request_with_activated_user_with_admin_role(self):
        """
        Ensure activated users with assigned `ADMIN` role can send POST
        requests to the `UnionUpdateView` view.
        """
        # Activate user
        self.admin.status = User.ACTIVE
        self.admin.save()

        customer = CustomerFactory(name='Test customer updated')
        payload = {
            'name': 'Test union updated',
            'customer': customer.pk
        }

        self.client.force_login(self.admin)
        response = self.client.post(self.url, payload, follow=True)
        expected_url = reverse('customers:union-list')

        self.union.refresh_from_db()

        # Assertions
        self.assertRedirects(response, expected_url)
        self.assertEqual(self.union.name, payload['name'])
        self.assertEqual(self.union.customer.pk, payload['customer'])

    def test_GET_request_with_activated_user_with_staff_role(self):
        """
        Ensure activated users with assigned `STAFF` role can access
        the `UnionUpdateView` view.
        """
        # Activate user
        self.staff.status = User.ACTIVE
        self.staff.save()

        self.client.force_login(self.staff)
        response = self.client.get(self.url)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

    def test_POST_request_with_activated_user_with_staff_role(self):
        """
        Ensure activated users with assigned `STAFF` role can send POST
        requests to the `UnionDeleteView` view.
        """
        # Activate user
        self.staff.status = User.ACTIVE
        self.staff.save()

        customer = CustomerFactory(name='Test customer updated')
        payload = {
            'name': 'Test union updated',
            'customer': customer.pk
        }

        self.client.force_login(self.staff)
        response = self.client.post(self.url, payload, follow=True)
        expected_url = reverse('customers:union-list')

        self.union.refresh_from_db()

        # Assertions
        self.assertRedirects(response, expected_url)
        self.assertEqual(self.union.name, payload['name'])
        self.assertEqual(self.union.customer.pk, payload['customer'])

    def test_GET_request_with_activated_user_with_management_role(self):
        """
        Ensure activated users with assigned `MANAGEMENT` role cannot access
        the `UnionUpdateView` view.
        """
        # Activate user
        self.management.status = User.ACTIVE
        self.management.save()

        self.client.force_login(self.management)
        response = self.client.get(self.url)

        # Assertions
        self.assertEqual(response.status_code, 403)

    def test_GET_request_with_activated_user_with_guest_role(self):
        """
        Ensure activated users with assigned `GUEST` role cannot access
        the `UnionUpdateView` view.
        """
        # Activate user
        self.guest.status = User.ACTIVE
        self.guest.save()

        self.client.force_login(self.guest)
        response = self.client.get(self.url)

        # Assertions
        self.assertEqual(response.status_code, 403)





class UnionDeleteViewTests(TestCase):
    """
    Tests for the `UnionDeleteView` test.
    """
    fixtures = ['roles', 'customers']

    def setUp(self):
        self.template = 'customers/modals/unions/union_delete_form.html'
        self.union = UnionFactory()
        self.url = reverse('customers:union-delete', args=[self.union.pk])
        self.user = UserFactory()
        self.admin = AdminUserFactory()
        self.management = ManagementUserFactory()
        self.staff = StaffUserFactory()
        self.guest = GuestUserFactory()

    def test_request_with_anonymous_user(self):
        """
        Ensure unauthenticated users cannot access the `UnionDeleteView` view.
        """
        response = self.client.get(self.url, follow=True)
        queryparam = f'/customers/unions/{self.union.pk}/delete/'
        expected_url = f'{reverse("accounts:login")}?next={queryparam}'

        # Assertions
        self.assertRedirects(response, expected_url)

    def test_GET_request_with_activated_user_with_admin_role(self):
        """
        Ensure activated users with assigned `ADMIN` role can access
        the `UnionDeleteView` view.
        """
        # Activate user
        self.admin.status = User.ACTIVE
        self.admin.save()

        self.client.force_login(self.admin)
        response = self.client.get(self.url)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

    def test_POST_request_with_activated_user_with_admin_role(self):
        """
        Ensure activated users with assigned `ADMIN` role can send POST
        requests to the `UnionDeleteView` view.
        """
        # Activate user
        self.admin.status = User.ACTIVE
        self.admin.save()

        customer = CustomerFactory(name='Test customer updated')
        payload = {
            'name': 'Test union updated',
            'customer': customer.pk
        }

        self.client.force_login(self.admin)
        response = self.client.post(self.url, payload, follow=True)
        expected_url = reverse('customers:union-list')

        # Assertions
        self.assertRedirects(response, expected_url)
        self.assertEqual(Union.objects.count(), 0)


    def test_GET_request_with_activated_user_with_staff_role(self):
        """
        Ensure activated users with assigned `STAFF` role can access
        the `UnionDeleteView` view.
        """
        # Activate user
        self.staff.status = User.ACTIVE
        self.staff.save()

        self.client.force_login(self.staff)
        response = self.client.get(self.url)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

    def test_POST_request_with_activated_user_with_staff_role(self):
        """
        Ensure activated users with assigned `STAFF` role can send POST
        requests to the `UnionDeleteView` view.
        """
        # Activate user
        self.staff.status = User.ACTIVE
        self.staff.save()

        customer = CustomerFactory(name='Test customer updated')
        payload = {
            'name': 'Test union updated',
            'customer': customer.pk
        }

        self.client.force_login(self.staff)
        response = self.client.post(self.url, payload, follow=True)
        expected_url = reverse('customers:union-list')

        # Assertions
        self.assertRedirects(response, expected_url)
        self.assertEqual(Union.objects.count(), 0)

    def test_GET_request_with_activated_user_with_management_role(self):
        """
        Ensure activated users with assigned `MANAGEMENT` role cannot access
        the `UnionDeleteView` view.
        """
        # Activate user
        self.management.status = User.ACTIVE
        self.management.save()

        self.client.force_login(self.management)
        response = self.client.get(self.url)

        # Assertions
        self.assertEqual(response.status_code, 403)

    def test_GET_request_with_activated_user_with_guest_role(self):
        """
        Ensure activated users with assigned `GUEST` role cannot access
        the `UnionDeleteView` view.
        """
        # Activate user
        self.guest.status = User.ACTIVE
        self.guest.save()

        self.client.force_login(self.guest)
        response = self.client.get(self.url)

        # Assertions
        self.assertEqual(response.status_code, 403)

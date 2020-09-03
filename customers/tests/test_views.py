from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.tests.factories import UserFactory, AdminUserFactory, \
    GuestUserFactory, ManagementUserFactory, StaffUserFactory


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
        # Disable user
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
        # Disable user
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
        # Disable user
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
        # Disable user
        self.admin.status = User.PENDING
        self.admin.save()

        self.client.force_login(self.admin)
        response = self.client.get(self.url)

        # Assertions
        self.assertEqual(response.status_code, 403)

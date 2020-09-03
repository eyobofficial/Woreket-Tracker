from django.test import TestCase
from django.urls import reverse

from accounts.tests.factories import UserFactory


class UnionListViewTests(TestCase):
    """
    Tests for the `UnionListView` test.
    """

    def setUp(self):
        self.template = 'customers/union_list.html'
        self.url = reverse('customers:union-list')
        self.user = UserFactory()

    def test_request_with_anonymous_user(self):
        """
        Ensure unauthenticated users cannot access the `UnionListView` view.
        """
        response = self.client.get(self.url, follow=True)
        expected_url = f'{reverse("accounts:login")}?next=/customers/unions/'

        # Assertions
        self.assertRedirects(response, expected_url)

    def test_request_with_authenticated_user(self):
        """
        Ensure authenticated users can access the `UnionListView` view.
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

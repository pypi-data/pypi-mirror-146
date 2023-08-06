from django.test import TestCase
from django.urls import reverse

from shatail.test.utils import ShatailTestUtils


class TestBulkActionDispatcher(TestCase, ShatailTestUtils):
    def setUp(self):

        # Login
        self.user = self.login()

    def test_bulk_action_invalid_action(self):
        url = reverse(
            "shatail_bulk_action",
            args=(
                "shatailcore",
                "page",
                "ships",
            ),
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

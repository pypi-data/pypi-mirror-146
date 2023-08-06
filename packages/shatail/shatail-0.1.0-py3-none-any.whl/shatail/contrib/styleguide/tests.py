from django.test import TestCase
from django.urls import reverse

from shatail.test.utils import ShatailTestUtils


class TestStyleGuide(TestCase, ShatailTestUtils):
    def setUp(self):
        self.login()

    def test_styleguide(self):
        response = self.client.get(reverse("shatailstyleguide"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shatailstyleguide/base.html")

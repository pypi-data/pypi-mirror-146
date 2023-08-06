from django.test import TestCase

from shatail.test.utils import ShatailTestUtils


class AdminAPITestCase(TestCase, ShatailTestUtils):
    def setUp(self):
        self.user = self.login()

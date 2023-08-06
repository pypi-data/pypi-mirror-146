from django.test import TestCase
from django.urls import reverse

from shatail.contrib.settings.registry import Registry
from shatail.test.testapp.models import NotYetRegisteredSetting
from shatail.test.utils import ShatailTestUtils


class TestRegister(TestCase, ShatailTestUtils):
    def setUp(self):
        self.registry = Registry()
        self.login()

    def test_register(self):
        self.assertNotIn(NotYetRegisteredSetting, self.registry)
        NowRegisteredSetting = self.registry.register_decorator(NotYetRegisteredSetting)
        self.assertIn(NotYetRegisteredSetting, self.registry)
        self.assertIs(NowRegisteredSetting, NotYetRegisteredSetting)

    def test_icon(self):
        admin = self.client.get(reverse("shatailadmin_home"))
        self.assertContains(admin, "icon-setting-tag")

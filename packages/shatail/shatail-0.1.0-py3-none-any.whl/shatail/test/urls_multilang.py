from __future__ import absolute_import, unicode_literals

from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path

from shatail import urls as shatail_urls

urlpatterns = i18n_patterns(path("", include(shatail_urls)))

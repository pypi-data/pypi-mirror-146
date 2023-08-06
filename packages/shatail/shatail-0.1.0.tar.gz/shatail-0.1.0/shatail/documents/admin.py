from django.conf import settings
from django.contrib import admin

from shatail.documents.models import Document

if (
    hasattr(settings, "SHATAILDOCS_DOCUMENT_MODEL")
    and settings.SHATAILDOCS_DOCUMENT_MODEL != "shataildocs.Document"
):
    # This installation provides its own custom document class;
    # to avoid confusion, we won't expose the unused shataildocs.Document class
    # in the admin.
    pass
else:
    admin.site.register(Document)

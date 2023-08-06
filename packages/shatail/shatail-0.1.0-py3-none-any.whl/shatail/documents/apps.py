from django.apps import AppConfig
from django.db.models import ForeignKey
from django.utils.translation import gettext_lazy as _

from . import get_document_model


class ShatailDocsAppConfig(AppConfig):
    name = "shatail.documents"
    label = "shataildocs"
    verbose_name = _("Shatail documents")
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        from shatail.documents.signal_handlers import register_signal_handlers

        register_signal_handlers()

        # Set up model forms to use AdminDocumentChooser for any ForeignKey to the document model
        from shatail.admin.forms.models import register_form_field_override

        from .widgets import AdminDocumentChooser

        Document = get_document_model()
        register_form_field_override(
            ForeignKey, to=Document, override={"widget": AdminDocumentChooser}
        )

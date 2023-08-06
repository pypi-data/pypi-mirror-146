from warnings import warn

from shatail.admin.panels import FieldPanel
from shatail.utils.deprecation import RemovedInShatail50Warning


class DocumentChooserPanel(FieldPanel):
    def __init__(self, *args, **kwargs):
        warn(
            "shatail.documents.edit_handlers.DocumentChooserPanel is obsolete and should be replaced by shatail.admin.panels.FieldPanel",
            category=RemovedInShatail50Warning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)

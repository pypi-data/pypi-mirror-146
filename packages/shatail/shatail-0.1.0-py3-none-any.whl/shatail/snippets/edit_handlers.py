from warnings import warn

from shatail.admin.panels import FieldPanel
from shatail.utils.deprecation import RemovedInShatail50Warning


class SnippetChooserPanel(FieldPanel):
    def __init__(self, *args, **kwargs):
        warn(
            "shatail.snippets.edit_handlers.SnippetChooserPanel is obsolete and should be replaced by shatail.admin.panels.FieldPanel",
            category=RemovedInShatail50Warning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)

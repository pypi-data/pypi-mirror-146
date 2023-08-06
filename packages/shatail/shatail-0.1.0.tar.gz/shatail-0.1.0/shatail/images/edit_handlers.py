from warnings import warn

from django.template.loader import render_to_string

from shatail.admin.compare import ForeignObjectComparison
from shatail.admin.panels import FieldPanel
from shatail.utils.deprecation import RemovedInShatail50Warning


class ImageChooserPanel(FieldPanel):
    def __init__(self, *args, **kwargs):
        warn(
            "shatail.images.edit_handlers.ImageChooserPanel is obsolete and should be replaced by shatail.admin.panels.FieldPanel",
            category=RemovedInShatail50Warning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)


class ImageFieldComparison(ForeignObjectComparison):
    def htmldiff(self):
        image_a, image_b = self.get_objects()

        return render_to_string(
            "shatailimages/widgets/compare.html",
            {
                "image_a": image_a,
                "image_b": image_b,
            },
        )

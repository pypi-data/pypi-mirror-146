from django import forms

from shatail.admin.widgets import AdminDateTimeInput
from shatail.documents.forms import BaseDocumentForm
from shatail.images.forms import BaseImageForm


class OverriddenWidget(forms.Widget):
    pass


class AlternateImageForm(BaseImageForm):
    form_only_field = forms.DateTimeField()

    class Meta:
        widgets = {
            **BaseImageForm.Meta.widgets,
            "tags": OverriddenWidget,
            "file": OverriddenWidget,
            "form_only_field": AdminDateTimeInput,
        }


class AlternateDocumentForm(BaseDocumentForm):
    form_only_field = forms.DateTimeField()

    class Meta:
        widgets = {
            "tags": OverriddenWidget,
            "file": OverriddenWidget,
            "form_only_field": AdminDateTimeInput,
        }

import json
import warnings

from django.forms import Media, widgets
from django.utils.functional import cached_property

from shatail.admin.rich_text.converters.contentstate import ContentstateConverter
from shatail.admin.staticfiles import versioned_static
from shatail.rich_text import features as feature_registry
from shatail.telepath import register
from shatail.widget_adapters import WidgetAdapter


class DraftailRichTextArea(widgets.HiddenInput):
    template_name = "shatailadmin/widgets/draftail_rich_text_area.html"
    is_hidden = False

    # this class's constructor accepts a 'features' kwarg
    accepts_features = True

    # Draftail has its own commenting
    show_add_comment_button = False

    def __init__(self, *args, **kwargs):
        # note: this constructor will receive an 'options' kwarg taken from the SHATAILADMIN_RICH_TEXT_EDITORS setting,
        # but we don't currently recognise any options from there (other than 'features', which is passed here as a separate kwarg)
        kwargs.pop("options", None)
        self.options = {}
        self.plugins = []

        self.features = kwargs.pop("features", None)
        if self.features is None:
            self.features = feature_registry.get_default_features()

        for feature in self.features:
            plugin = feature_registry.get_editor_plugin("draftail", feature)
            if plugin is None:
                warnings.warn(
                    f"Draftail received an unknown feature '{feature}'.",
                    category=RuntimeWarning,
                )
            else:
                plugin.construct_options(self.options)
                self.plugins.append(plugin)

        self.converter = ContentstateConverter(self.features)

        default_attrs = {"data-draftail-input": True}
        attrs = kwargs.get("attrs")
        if attrs:
            default_attrs.update(attrs)
        kwargs["attrs"] = default_attrs

        super().__init__(*args, **kwargs)

    def format_value(self, value):
        # Convert database rich text representation to the format required by
        # the input field
        value = super().format_value(value)

        if value is None:
            value = ""

        return self.converter.from_database_format(value)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["options_json"] = json.dumps(self.options)
        return context

    def value_from_datadict(self, data, files, name):
        original_value = super().value_from_datadict(data, files, name)
        if original_value is None:
            return None
        return self.converter.to_database_format(original_value)

    @cached_property
    def media(self):
        media = Media(
            js=[
                versioned_static("shatailadmin/js/draftail.js"),
            ],
            css={"all": [versioned_static("shatailadmin/css/panels/draftail.css")]},
        )

        for plugin in self.plugins:
            media += plugin.media

        return media


class DraftailRichTextAreaAdapter(WidgetAdapter):
    js_constructor = "shatail.widgets.DraftailRichTextArea"

    def js_args(self, widget):
        return [
            widget.options,
        ]


register(DraftailRichTextAreaAdapter(), DraftailRichTextArea)

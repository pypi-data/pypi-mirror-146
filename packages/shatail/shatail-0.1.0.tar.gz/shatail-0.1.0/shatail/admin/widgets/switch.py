from django.forms import widgets


class SwitchInput(widgets.CheckboxInput):
    template_name = "shatailadmin/widgets/switch.html"

from django.forms import CheckboxInput

class FormStyleMixin:
    default_input_class = "form-control"
    default_checkbox_class = "form-check-input"
    placeholder_fields = {}

    def _update_widget_attrs(self, field_name, field):
        widget = field.widget
        attrs = widget.attrs

        # Добавляем css-класс
        if field.widget.__class__.__name__ in ["CheckboxInput"]:
            attrs["class"] = self.default_checkbox_class
        else:
            attrs["class"] = self.default_input_class

        # Добавляем placeholder, если он указан
        if field_name in self.placeholder_fields:
            attrs["placeholder"] = self.placeholder_fields[field_name]

        widget.attrs = attrs

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            self._update_widget_attrs(field_name, field)

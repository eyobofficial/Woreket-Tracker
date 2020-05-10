from django import forms


class FormattedNumberField(forms.DecimalField):
    """Comma separated decimal field."""

    def to_python(self, value):
        value = value.replace(',', '')
        return super().to_python(value)

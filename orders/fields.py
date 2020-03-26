from django import forms


class MoneyField(forms.DecimalField):
    """Comma separated decimal field."""

    def to_python(self, value):
        value = value.replace(',', '')
        return super().to_python(value)

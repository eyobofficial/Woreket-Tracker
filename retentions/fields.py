from django import forms


class MoneyField(forms.DecimalField):
    """Normalizes a comma separated money to a decimal field."""

    def to_python(self, value):
        value = value.replace(',', '')
        return super().to_python(value)

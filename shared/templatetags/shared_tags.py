from django import template

register = template.Library()


@register.filter(name='whole_part')
def whole_part(value):
    """Returns the whole number part of a decimal.

    Args:
        value (Decimal): A decimal number

    Returns:
        whole_num (str): A whole number part of the decimal
    """
    num = str(value)
    whole, _ = num.split('.')
    return whole


@register.filter(name='decimal_part')
def decimal_part(value):
    """Returns the decimal part of a number.

    Args:
        value (Decimal): A decimal number

    Returns:
        decimal_num (str): A decimal number part of the number
    """
    num = str(value)
    _, decimal = num.split('.')
    return decimal

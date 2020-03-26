from shared.mixins import BaseLoggedInView


class BaseOrderView(BaseLoggedInView):
    """
    Base view for all `orders` app views.
    """
    page_name = 'delivery-orders'

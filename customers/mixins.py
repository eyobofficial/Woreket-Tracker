from shared.mixins import BaseAccessMixin


class BaseCustomersView(BaseAccessMixin):
    """
    Base view for all `customers` app views.
    """
    page_name = None
    access_roles = []

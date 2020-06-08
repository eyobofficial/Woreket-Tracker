from shared.mixins import BaseAccessMixin


class BaseOrderView(BaseAccessMixin):
    """
    Base view for all `orders` app views.
    """
    page_name = 'delivery-orders'
    access_roles = []


class BaseBatchesView(BaseAccessMixin):
    """
    Base view for all `Batch` model views.
    """
    page_name = 'batches'
    access_roles = []

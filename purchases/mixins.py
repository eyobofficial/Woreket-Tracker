from shared.mixins import BaseAccessMixin


class BasePurchasesView(BaseAccessMixin):
    """
    Base view for all `purchses` app views.
    """
    page_name = None
    access_roles = []

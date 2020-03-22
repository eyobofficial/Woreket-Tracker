from shared.mixins import BaseLoggedInView


class BaseAllocationView(BaseLoggedInView):
    """
    Base view for all `allocations` app views.
    """
    page_name = 'Allocations'

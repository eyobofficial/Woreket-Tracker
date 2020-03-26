from shared.mixins import BaseLoggedInView


class BaseRetentionView(BaseLoggedInView):
    """
    Base view for all `retentions` app views.
    """
    page_name = 'Retention'

from shared.mixins import BaseAccessMixin


class AccountMixin(BaseAccessMixin):
    """Base view mixin to restricted account app views."""
    page_name = 'accounts'

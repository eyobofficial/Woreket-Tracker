from shared.mixins import BaseAccessMixin


class BaseUsersView(BaseAccessMixin):
    """
    Base view for all `uers` app views.
    """
    page_name = 'users'
    access_roles = []

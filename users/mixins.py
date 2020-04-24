from django.contrib.auth import get_user_model

from shared.constants import ROLE_ADMIN
from shared.mixins import BaseAccessMixin


User = get_user_model()


class BaseUserView(BaseAccessMixin):
    """
    Base view for all `uers` app views.
    """
    page_name = 'users'
    access_roles = [ROLE_ADMIN]


class BaseUserEditView(BaseUserView):
    """
    Base view for user related generic and edit views.
    """
    model = User
    queryset = User.objects.filter(is_active=True, is_superuser=False)

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.exclude(pk=self.request.user.pk)
        return qs


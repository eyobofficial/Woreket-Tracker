from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import ContextMixin


class BaseView(ContextMixin):
    """
    Base view for all views.
    """
    page_name = None

    def get_context_data(self, **kwargs):
        kwargs.update(page_name=self.page_name)
        return super().get_context_data(**kwargs)


class BaseLoggedInView(LoginRequiredMixin, BaseView):
    """
    Base logged view for all views.
    """
    pass

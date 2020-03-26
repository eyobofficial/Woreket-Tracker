from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy

from shared.models import Product

from .forms import CreditLetterForm
from .mixins import BaseRetentionView
from .models import CreditLetter


class RetentionOverview(BaseRetentionView, TemplateView):
    template_name = 'retentions/overview.html'


class CreditLetterCreateView(BaseRetentionView, CreateView):
    """
    Creates new Letter of credit instance.
    """
    template_name = 'retentions/modals/lc_create.html'
    form_class = CreditLetterForm
    success_url = reverse_lazy('retentions:overview')

    def get_context_data(self, **kwargs):
        kwargs.update({
            'product_list': Product.objects.all()
        })
        return super().get_context_data(**kwargs)

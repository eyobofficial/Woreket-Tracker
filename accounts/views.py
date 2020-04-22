from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import UserRegistrationForm


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy('accounts:register-success')
    template_name = 'registration/register.html'


class RegistrationSuccessView(TemplateView):
    template_name = 'registration/success.html'

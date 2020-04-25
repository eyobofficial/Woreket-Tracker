from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
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


class CustomPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    template_name='registration/password_form.html'
    success_url = reverse_lazy('accounts:password-change')
    success_message = 'Password changed successfully.'

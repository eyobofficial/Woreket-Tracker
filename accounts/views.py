from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from shared.constants import ROLE_SUPPLIER

from .forms import UserRegistrationForm, ProfileUpdateForm
from .mixins import AccountMixin


User = get_user_model()


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy('accounts:register-success')
    template_name = 'registration/register.html'


class RegistrationSuccessView(TemplateView):
    template_name = 'registration/success.html'


class PasswordUpdateView(AccountMixin, SuccessMessageMixin, PasswordChangeView):
    template_name='registration/password_form.html'
    success_url = reverse_lazy('accounts:password-change')
    success_message = 'Password changed successfully.'
    access_roles = '__all__'


class ProfileUpdateView(AccountMixin, SuccessMessageMixin, UpdateView):
    template_name = 'registration/profile_form.html'
    model = User
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('accounts:profile-update')
    success_message = 'Your profile is updated successfully.'
    access_roles = '__all__'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        kwargs.update(ROLE_SUPPLIER=ROLE_SUPPLIER)
        return super().get_context_data(**kwargs)

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, UpdateView

from shared.constants import ROLE_STAFF, ROLE_SUPPLIER, DEMO, ROLE_GUEST

from .forms import UserRegistrationForm, ProfileUpdateForm
from .mixins import AccountMixin
from .models import CustomUser


User = get_user_model()


class CustomLoginView(LoginView):

    def get_success_url(self):
        """
        Returns the user profile url if the user has not activated,
        else return the default success url.
        """
        success_url = super().get_success_url()
        user = self.request.user
        if user.is_superuser:
            return success_url
        elif user.status == CustomUser.PENDING or user.role is None:
            return reverse('accounts:profile-update')
        else:
            return success_url


class UserRegistrationView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('accounts:register-success')
    template_name = 'registration/register.html'

    def get_success_message(self, cleaned_data):
        if settings.ENVIRONMENT == DEMO:
            return 'Please login with your new e-mail and password.'
        return super().get_success_message(cleaned_data)

    def get_success_url(self):
        success_url = super().get_success_url()
        if settings.ENVIRONMENT == DEMO:
            return reverse('accounts:login')
        return success_url

    def form_valid(self, form):
        """
        When the environment is `DEMO`, activate the
        user and assign him/her a staff role.
        """
        redirect_url = super().form_valid(form)
        user = self.object
        role = ROLE_GUEST
        status = CustomUser.PENDING
        if settings.ENVIRONMENT == DEMO:
            role = ROLE_ADMIN
            status = CustomUser.ACTIVE
        user.role = role
        user.status = status
        user.save()
        return redirect_url


class RegistrationSuccessView(TemplateView):
    template_name = 'registration/success.html'


class PasswordUpdateView(SuccessMessageMixin, PasswordChangeView):
    template_name='registration/password_form.html'
    success_url = reverse_lazy('accounts:password-change')
    success_message = 'Password changed successfully.'
    page_name = 'accounts'
    access_roles = '__all__'


class ProfileUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'registration/profile_form.html'
    model = User
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('accounts:profile-update')
    success_message = 'Your profile is updated successfully.'
    page_name = 'accounts'
    access_roles = '__all__'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        kwargs.update(ROLE_SUPPLIER=ROLE_SUPPLIER)
        return super().get_context_data(**kwargs)

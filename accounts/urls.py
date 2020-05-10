from django.contrib.auth import views as auth_views
from django.urls import path, include

from .views import UserRegistrationView, RegistrationSuccessView, \
    PasswordUpdateView, ProfileUpdateView, CustomLoginView


app_name = 'accounts'


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path(
        'password-change/',
        PasswordUpdateView.as_view(),
        name='password-change'
    ),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path(
        'register/success/',
        RegistrationSuccessView.as_view(),
        name='register-success'
    ),
    path('profile/', ProfileUpdateView.as_view(), name='profile-update')
]

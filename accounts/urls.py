from django.contrib.auth import views as auth_views
from django.urls import path, include

from .views import UserRegistrationView, RegistrationSuccessView, \
    CustomPasswordChangeView


app_name = 'accounts'


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path(
        'password-change/',
        CustomPasswordChangeView.as_view(),
        name='password-change'
    ),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path(
        'register/success/',
        RegistrationSuccessView.as_view(),
        name='register-success'
    )
]

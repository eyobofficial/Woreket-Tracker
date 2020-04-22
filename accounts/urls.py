from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from .views import UserRegistrationView, RegistrationSuccessView


app_name = 'accounts'


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path(
        'register/success/',
        RegistrationSuccessView.as_view(),
        name='register-success'
    )
]

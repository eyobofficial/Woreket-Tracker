from django.urls import path

from .views import UserListView, UserDetailView, UserUpdateView, \
    UserActivateView, UserDeactivateView


app_name = 'users'

urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('<uuid:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('<uuid:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path(
        '<uuid:pk>/activate/',
        UserActivateView.as_view(),
        name='user-activate'
    ),
    path(
        '<uuid:pk>/deactivate/',
        UserDeactivateView.as_view(),
        name='user-deactivate'
    ),
]

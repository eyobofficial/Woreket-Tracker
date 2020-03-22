from django.urls import path

from .views import DistributionListView, DistributionDetailView, \
    DistributionCreateView, AllocationCreateView


app_name = 'allocations'


urlpatterns = [
    path('', DistributionListView.as_view(), name='distribution-list'),
    path(
        '<uuid:pk>/',
        DistributionDetailView.as_view(),
        name='distribution-detail'
    ),
    path(
        'create/',
        DistributionCreateView.as_view(),
        name='distribution-create'
    ),
    path(
        '<uuid:pk>/allocations/create/',
        AllocationCreateView.as_view(),
        name='allocation-create'
    )
]

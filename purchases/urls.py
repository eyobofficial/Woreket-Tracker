from django.urls import path

from .views import BatchListView, BatchCreateView, BatchUpdateView, \
    BatchDeleteView, BatchDetailView


app_name = 'purchases'

urlpatterns = [
    path('batches/', BatchListView.as_view(), name='batch-list'),
    path('batches/create/', BatchCreateView.as_view(), name='batch-create'),
    path('batches/<uuid:pk>/', BatchDetailView.as_view(), name='batch-detail'),
    path(
        'batches/<uuid:pk>/update/',
        BatchUpdateView.as_view(),
        name='batch-update'
    ),
    path(
        'batches/<uuid:pk>/delete/',
        BatchDeleteView.as_view(),
        name='batch-delete'
    )
]

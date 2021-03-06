from django.urls import path

from .views import UnionListView, UnionCreateView, UnionUpdateView, \
    UnionDeleteView


app_name = 'customers'

urlpatterns = [
    path('unions/', UnionListView.as_view(), name='union-list'),
    path('unions/create/', UnionCreateView.as_view(), name='union-create'),
    path(
        'unions/<uuid:pk>/update/',
        UnionUpdateView.as_view(),
        name='union-update'
    ),
    path(
        'unions/<uuid:pk>/delete/',
        UnionDeleteView.as_view(),
        name='union-delete'
    )
]

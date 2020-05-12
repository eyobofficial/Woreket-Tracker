from django.urls import path

from .views import UnionListView, UnionCreateView


app_name = 'customers'

urlpatterns = [
    path('unions/', UnionListView.as_view(), name='union-list'),
    path('unions/create/', UnionCreateView.as_view(), name='union-create'),
]

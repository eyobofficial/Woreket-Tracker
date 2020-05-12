from django.urls import path

from .views import UnionListView


app_name = 'customers'

urlpatterns = [
    path('unions/', UnionListView.as_view(), name='union-list'),
]

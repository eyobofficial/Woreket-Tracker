from django.urls import path

from .views import RetentionOverview, CreditLetterCreateView


app_name = 'retentions'


urlpatterns = [
    path('', RetentionOverview.as_view(), name='overview'),
    path('lc/create/', CreditLetterCreateView.as_view(), name='lc-create'),
]

app_name = 'broadcast'
from . import views
from django.urls import path

urlpatterns = [
    path('email/', views.EmailBroadCastApi.as_view(), name='emailbroadcast'),
    path('phone/', views.SmsBroadcastApi.as_view(), name='emailbroadcast')
]
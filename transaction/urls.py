from django.urls import path
from . import views

urlpatterns = [
    path('', views.TransactionListAPIView.as_view(), name='transaction-list'),
    path('total/stats/', views.GetTransactionStatistics.as_view(), name='total-deposit'),
    path('all/', views.AllTransactionApiView.as_view(), name='all-transactions')
]
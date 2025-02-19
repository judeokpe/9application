from django.urls import path
from .views import TradingSettingsAPIView, TradingSettingsCreateAPIView

urlpatterns = [
    path('settings/<int:pk>/', TradingSettingsAPIView.as_view(), name='trading-settings-detail'),
    path('settings/', TradingSettingsCreateAPIView.as_view(), name='trading-settings-create'),
]

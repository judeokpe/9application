from django.urls import path
from . import views

app_name = 'exec'

urlpatterns = [
    path('users/list/', views.UserListApi.as_view(), name='user'),
    path('coin/disable/', views.DisableToken.as_view(), name='disablecoin'),
    path('coin/enable/', views.EnableToken.as_view(), name='enabletoken'),
    path('user/stats/', views.GetUserActivityStatisticsApi.as_view(), name='getuserstatistics '),
    path('user/settings/<uuid:id>/', views.UserTradingSettings.as_view(), name='gettradingsettings')
]

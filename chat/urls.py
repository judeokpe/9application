from django.urls import path
from . import views


urlpatterns = [
    path('messages/<str:uid>/', views.GetChatMessageApi.as_view(), name='messages'),
    path('get-user-threads/', views.GetUserThreads.as_view(), name='get-user-threads'),
]
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.BankInformationListCreateView.as_view(), name='bank-information-list-create'),
#     path('<int:pk>/', views.BankInformationDetailView.as_view(), name='bank-information-detail'),
# ]
from django.urls import path
from .views import BankInformationListCreateView, BankInformationDetailView

urlpatterns = [
    path('', BankInformationListCreateView.as_view(), name='bank-information-list-create'),
    path('<uuid:pk>/', BankInformationDetailView.as_view(), name='bank-information-detail'),
]

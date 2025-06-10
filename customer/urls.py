# customer/urls.py
from django.urls import path
from . import views

app_name = 'customer' # Namespace for customer URLs

urlpatterns = [
    path('register/', views.CustomerRegistrationView.as_view(), name='register'),
    path('login/', views.CustomerLoginView.as_view(), name='login'),
    # Customer actions
    path('supplies/', views.AvailableSupplyListView.as_view(), name='available_supplies'),
    path('request/new/', views.CustomerRequestCreateView.as_view(), name='request_create'),
    path('my_requests/', views.MyRequestsListView.as_view(), name='my_requests_list'),
]

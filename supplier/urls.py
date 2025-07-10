from django.urls import path
from . import views

app_name = 'supplier'

urlpatterns = [
    path('register/', views.supplier_register, name='supplier_register'),
    path('login/', views.supplier_login, name='supplier_login'),
    path('dashboard/', views.supplier_dashboard, name='supplier_dashboard'),
]

# supply/urls.py
from django.urls import path
from supply import views # Use relative import

app_name = 'supply' # Namespace for supply app URLs

urlpatterns = [
    # Keep dashboard/index if needed, or remove if dashboard is global
    # path('', views.dashboard, name='index'), # Example if index was here

    # Supplier URLs
    path('suppliers/', views.SupplierListView.as_view(), name='suppliers_list'),
    path('suppliers/add/', views.SupplierCreateView.as_view(), name='supplier_add'),
    path('suppliers/<int:pk>/edit/', views.SupplierUpdateView.as_view(), name='supplier_edit'),
    path('suppliers/<int:pk>/delete/', views.SupplierDeleteView.as_view(), name='supplier_delete'),
    path('suppliers/<int:pk>/', views.SupplierDetailView.as_view(), name='supplier_detail'),

    # Supply Item URLs
    path('items/', views.SupplyItemListView.as_view(), name='supplyitem_list'),
    path('items/add/', views.SupplyItemCreateView.as_view(), name='supplyitem_add'),
    path('items/<int:pk>/edit/', views.SupplyItemUpdateView.as_view(), name='supplyitem_edit'),
    path('items/<int:pk>/delete/', views.SupplyItemDeleteView.as_view(), name='supplyitem_delete'),
    path('items/<int:pk>/', views.SupplyItemDetailView.as_view(), name='supplyitem_detail'),

    # Supply Transaction URLs
    path('transactions/', views.SupplyTransactionListView.as_view(), name='supplytransaction_list'),
    path('transactions/add/', views.SupplyTransactionCreateView.as_view(), name='supplytransaction_add'),
    path('transactions/<int:pk>/edit/', views.SupplyTransactionUpdateView.as_view(), name='supplytransaction_edit'),
    path('transactions/<int:pk>/delete/', views.SupplyTransactionDeleteView.as_view(), name='supplytransaction_delete'),
    path('transactions/<int:pk>/', views.SupplyTransactionDetailView.as_view(), name='supplytransaction_detail'),

    # Category URLs
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='category_add'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),

    # --- Manager Views for Customer Requests ---
    path('manager/requests/approved/', views.ApprovedRequestListView.as_view(), name='approved_requests_list'), # New URL for approved requests
    path('requests/pending/', views.CustomerRequestPendingForApprovalListView.as_view(), name='request_pending_list'),
    path('requests/all/', views.CustomerRequestAllListView.as_view(), name='request_all_list'),
    path('requests/approve/<int:pk>/', views.approve_customer_request, name='approve_request'),
    path('requests/reject/<int:pk>/', views.reject_customer_request, name='reject_request'),
    path('requests/deliver/<int:pk>/', views.mark_as_delivered, name='deliver_request'),
    path('requests/cancel-delivery/<int:pk>/', views.cancel_delivery_action, name='cancel_delivery'), # Use the updated view name
    path('notifications/mark_as_read/', views.mark_notifications_as_read, name='mark_notifications_as_read'),
]

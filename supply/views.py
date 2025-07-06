from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import *
from django.utils.decorators import method_decorator
from supply.models import *
from customer.models import *
from supply.forms import *
from customer.forms import *

# Create your views here.

@login_required
def dashboard(request):
    # Get counts for all statuses
    status_list = ['pending', 'approved', 'rejected', 'delivered']
    status_counts = {}
    for status in status_list:
        status_counts[status] = CustomerRequest.objects.filter(status=status).count()
    supply_items = SupplyItem.objects.all().count()
    context = {
        'delivered_total': status_counts['delivered'],
        'pending_total': status_counts['pending'],
        'approved_total': status_counts['approved'],
        'rejected_total': status_counts['rejected'],
        'supply_items': supply_items,
    }
    return render(request, 'supply/dashboard/dashboard.html', context)

#region #########   Authentication Views   ###################
# --- Keep is_supplier_manager function ---
def is_supplier_manager(user):
    """Checks if the user is a supply manager or a superuser."""
     # Check if authenticated and either a superuser or in the 'Supply Manager' group
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='Supply Manager').exists())

def is_customer(user):
    """Checks if the user is a customer."""
     # Check if authenticated and in the 'Customer' group
    return user.is_authenticated and user.groups.filter(name='Customer').exists()

# --- Mixins for Class-Based Views ---
class ManagerAccessMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to ensure user is a supply manager or superuser."""
    def test_func(self):
        return is_supplier_manager(self.request.user)
    
    def handle_no_permission(self):
        messages.error(self.request, "Access Denied: This page is for Supply Managers only.")
        # Redirect customers trying to access manager pages back to their area
        if is_customer(self.request.user):
            return redirect('customer:available_supplies')
        # Redirect any other non-manager/non-superuser to the customer login
        # (or a general landing page if you prefer)
        return redirect('customer:login')

class CustomerAccessMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to ensure user is a customer."""
    def test_func(self):
        return is_customer(self.request.user)
    
    # Override handle_no_permission for better UX
    def handle_no_permission(self):
        messages.error(self.request, "Access Denied: This page is for Customers only.")
        # Redirect managers trying to access customer pages back to the main dashboard
        if is_supplier_manager(self.request.user):
            return redirect('supply/dashboard/dashboard.html') # The main dashboard view name
        # Redirect any other non-customer to the customer login
        return redirect('customer:login')



#endregion ######### Authentication Views ###################

#region #########   Login/Logout Views   ###################
def login_page(request):
    if request.user.is_authenticated:
        return redirect('supply:supply_dashboard')  # Redirect to the dashboard if already logged in

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('supply:supply_dashboard')  # Redirect to the dashboard after login
    else:
        form = AuthenticationForm()

    return render(request, 'supply/auth/login.html', {'form': form})

@login_required
def logout_page(request):
    logout(request)
    # return render(request, 'supply/auth/logout.html')  # Render the logout confirmation page
    messages.info(request, "You have been successfully logged out.")
    # Redirect using the LOGOUT_REDIRECT_URL setting from settings.py
    return redirect(settings.LOGOUT_REDIRECT_URL)

@login_required
def index(request):
    if is_customer(request.user):
        # Redirect customers directly to their relevant page
        return redirect('customer:available_supplies')
    elif is_supplier_manager(request.user): # This includes superusers now
        # Keep managers/admins on the main dashboard
        return render(request, 'supply:supply_dashboard')
    else:
        # Fallback for authenticated users with no assigned role.
        logout(request)
        messages.warning(request, "Your account doesn't have a role assigned. You have been logged out. Please contact support or try logging in again if you have multiple roles.")
        return redirect('manager_login')
     # elif request.user.user_type == 'supply_manager' or request.user.is_superuser:
     #     # Keep managers/admins on the main dashboard or redirect to a specific manager dashboard
     #     return render(request, 'supply/dashboard/dashboard.html')

#endregion ######### Login/Logout Views ###################

#region #########   Supplier Views           ###################
class SupplierListView(ManagerAccessMixin, ListView):
    model = Supplier
    template_name = 'supply/suppliers/supplier_list.html'
    context_object_name = 'suppliers'
    paginate_by = 25

class SupplierCreateView(ManagerAccessMixin,CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'supply/suppliers/supplier_form.html'
    success_url = reverse_lazy('suppliers_list')

class SupplierUpdateView(ManagerAccessMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'supply/suppliers/supplier_form.html'
    success_url = reverse_lazy('suppliers_list')

class SupplierDeleteView(ManagerAccessMixin,DeleteView):
    model = Supplier
    template_name = 'supply/suppliers/supplier_confirm_delete.html'
    success_url = reverse_lazy('suppliers_list')
    
class SupplierDetailView(ManagerAccessMixin, DetailView):
    model = Supplier
    template_name = 'supply/supplier_detail.html'
    context_object_name = 'supplier'
#endregion ######### Supplier Views ###################

#region #########   SupplyItem Views         ###################
class SupplyItemListView(ManagerAccessMixin, ListView):
    model = SupplyItem
    template_name = 'supply/supply_items/supplyitem_list.html'
    context_object_name = 'supply_items'
    paginate_by = 25

class SupplyItemCreateView(ManagerAccessMixin, CreateView):
    model = SupplyItem
    form_class = SupplyItemForm
    template_name = 'supply/supply_items/supplyitem_form.html'
    success_url = reverse_lazy('supply:supplyitem_list')

class SupplyItemUpdateView(ManagerAccessMixin, UpdateView):
    model = SupplyItem
    form_class = SupplyItemForm
    template_name = 'supply/supply_items/supplyitem_form.html'
    success_url = reverse_lazy('supply:supplyitem_list')

class SupplyItemDeleteView(ManagerAccessMixin, DeleteView):
    model = SupplyItem
    template_name = 'supply/supply_items/supplyitem_confirm_delete.html'
    success_url = reverse_lazy('supply:supplyitem_list')
    
class SupplyItemDetailView(ManagerAccessMixin, DetailView):
    model = SupplyItem
    template_name = 'supply/supply_items/supplyitem_detail.html'
    context_object_name = 'supply_item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the transaction type from the query parameters
        transaction_type = self.request.GET.get('transaction_type')
        if transaction_type in ['supply_in', 'supply_out']:
            transactions = SupplyTransaction.objects.filter(
                supply_item=self.object, transaction_type=transaction_type
            )
        else:
            transactions = SupplyTransaction.objects.filter(supply_item=self.object)
        context['transactions'] = transactions
        context['selected_transaction_type'] = transaction_type
        return context
    



#endregion ######### SupplyItem Views ###################

#region #########   SupplyTransaction Views  ###################
class SupplyTransactionListView(ManagerAccessMixin, ListView):
    model = SupplyTransaction
    template_name = 'supply/supply_transaction/supplytransaction_list.html'
    context_object_name = 'supply_transactions'
    paginate_by = 25

class SupplyTransactionCreateView(ManagerAccessMixin,CreateView):
    model = SupplyTransaction
    form_class = SupplyTransactionForm
    template_name = 'supply/supply_transaction/supplytransaction_form.html'
    success_url = reverse_lazy('supply:supplytransaction_list')
    
    def form_valid(self, form):
        transaction = form.save(commit=False)
        if transaction.transaction_type == 'supply_out' and transaction.quantity > transaction.supply_item.quantity_in_stock:
            messages.error(self.request, "Not enough supplies to complete this transaction.")
            return redirect('supplytransaction_add')  # Redirect back to the form
        return super().form_valid(form)

class SupplyTransactionUpdateView(ManagerAccessMixin, UpdateView):
    model = SupplyTransaction
    form_class = SupplyTransactionForm
    template_name = 'supply/supply_transaction/supplytransaction_form.html'
    success_url = reverse_lazy('supply:supplytransaction_list')

class SupplyTransactionDeleteView(ManagerAccessMixin, DeleteView):
    model = SupplyTransaction
    template_name = 'supply/supply_transaction/supplytransaction_confirm_delete.html'
    success_url = reverse_lazy('supply:supplytransaction_list')

class SupplyTransactionDetailView(ManagerAccessMixin, DetailView):
    model = SupplyTransaction
    template_name = 'supply/supplytransaction_detail.html'
    context_object_name = 'supply:supply_transaction'
    
#endregion #################SupplyTransaction Views###################
    
#region #########   Category Views           ###################
class CategoryListView(ManagerAccessMixin, ListView):
    model = Category
    template_name = 'supply/category/category_list.html'
    context_object_name = 'categories'
    paginate_by = 25

class CategoryCreateView(ManagerAccessMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'supply/category/category_form.html'
    success_url = reverse_lazy('supply:category_list')

class CategoryUpdateView(ManagerAccessMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'supply/category/category_form.html'
    success_url = reverse_lazy('supply:category_list')

class CategoryDeleteView(ManagerAccessMixin, DeleteView):
    model = Category
    template_name = 'supply/category/category_confirm_delete.html'
    success_url = reverse_lazy('supply:category_list') 

class CategoryDetailView(ManagerAccessMixin, DetailView):
    model = Category
    template_name = 'supply/category/category_detail.html'
    context_object_name = 'category'    
#endregion ######### Category Views ########################

#region #########   Customer Request Views  ###################

class CustomerRequestPendingForApprovalListView(ManagerAccessMixin, ListView): # Add LoginRequiredMixin
    model = CustomerRequest
    template_name = 'supply/manager/request_pending_list.html'
    context_object_name = 'customer_requests'
    paginate_by = 20

    def get_queryset(self):
        # Only show requests with a status of "pending"
        return CustomerRequest.objects.filter(status='pending').order_by('request_date') # Order by oldest first

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Pending Customer Requests"
        context['form'] = RejectionReasonForm()  # Add the form to the context
        return context
    
# View for managers to see ALL requests (or approved/delivered)
class CustomerRequestAllListView(ManagerAccessMixin, ListView): # Renamed for clarity
    model = CustomerRequest
    template_name = 'supply/manager/request_all_list.html' # New template path
    context_object_name = 'customer_requests'
    paginate_by = 20

    # Optional: Restrict access
    # @method_decorator(user_passes_test(is_supplier_manager))
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        # Show all requests, maybe filter out pending or order differently
        return CustomerRequest.objects.all().order_by('-request_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "All Customer Requests"
        # Add rejection form for modal (if using modals)
        context['rejection_form'] = RejectionReasonForm()
        return context


@login_required
@user_passes_test(is_supplier_manager) # Uncomment if needed
def approve_customer_request(request, pk):
    # Use CustomerRequest from customer.models
    customer_request = get_object_or_404(CustomerRequest, pk=pk)
    if customer_request.status == 'pending':
        # Check stock before approving (important!)
        if customer_request.requested_quantity > customer_request.supply_item.quantity_in_stock:
             messages.error(request, f"Cannot approve: Insufficient stock for {customer_request.supply_item.item_name}. Available: {customer_request.supply_item.quantity_in_stock}")
             return redirect('supply:request_pending_list') # Redirect back

        customer_request.status = 'approved'
        customer_request.performed_by = request.user # Record who approved
        customer_request.save()
        messages.success(request, f"Request for {customer_request.supply_item.item_name} by {customer_request.customer.username} approved.")
    else:
        messages.warning(request, "Request is not in 'pending' state.")
    # Redirect to the pending list
    return redirect('supply:request_pending_list')

@login_required
@user_passes_test(is_supplier_manager)
def reject_customer_request(request, pk):
    # Use CustomerRequest from customer.models
    customer_request = get_object_or_404(CustomerRequest, pk=pk)
    if request.method == 'POST':
        form = RejectionReasonForm(request.POST, instance=customer_request)
        if form.is_valid() and customer_request.status == 'pending':
            # Update the status and save the form
            customer_request.status = 'rejected'
            customer_request.performed_by = request.user
            form.save()  # Save the form, which includes the rejection_reason
            customer_request.save()  # Save the updated status and performed_by
            messages.success(request, f"Request ID {customer_request.pk} for {customer_request.supply_item.item_name} rejected.")
        elif customer_request.status != 'pending':
            messages.warning(request, "Request is not in 'pending' state.")
        else:
            messages.error(request, "Please provide a valid reason for rejection.")
    else:
        messages.error(request, "Invalid request method for rejection.")
    # Redirect to the pending list
    return redirect('supply:request_pending_list')

@login_required
@user_passes_test(is_supplier_manager) # Uncomment if needed
def mark_as_delivered(request, pk):
    # Use CustomerRequest from customer.models
    customer_request = get_object_or_404(CustomerRequest, pk=pk)

    if request.method == 'POST': # Ensure it's a POST request if using the form method
        # Check if the request is in the 'approved' state before marking delivered
        if customer_request.status == 'approved':
            # Check stock just before marking delivered as a final safeguard
            if customer_request.requested_quantity > customer_request.supply_item.quantity_in_stock:
                messages.error(request, f"Cannot deliver: Insufficient stock for {customer_request.supply_item.item_name}. Available: {customer_request.supply_item.quantity_in_stock}")
                return redirect('supply:approved_requests_list') # Redirect back

            customer_request.status = 'delivered'
            customer_request.performed_by = request.user # Record who marked as delivered
            customer_request.save()
            messages.success(request, f"Request {pk} marked as delivered.")
            # Redirect back to the approved list or all list
            return redirect('supply:approved_requests_list') # Redirect back to the approved list
        else:
            messages.error(request, "Only approved requests can be marked as delivered.")
            # return redirect('supply:approved_requests_list') # Or wherever appropriate
            # Redirect back to the list where the action was likely initiated
            return redirect(request.META.get('HTTP_REFERER', 'supply:approved_requests_list'))
    else:
        # If accessed via GET, maybe redirect or show an error
        messages.error(request, "Invalid method for marking as delivered.")
        return redirect('supply:approved_requests_list')


# View for managers to see only APPROVED requests
class ApprovedRequestListView(ManagerAccessMixin, ListView):
    model = CustomerRequest
    template_name = 'supply/manager/request_approved_list.html' # New template
    context_object_name = 'customer_requests'
    paginate_by = 20 # Optional pagination

    def get_queryset(self):
        # Filter requests to show only those with status 'approved'
        return CustomerRequest.objects.filter(status='approved').select_related('customer', 'supply_item').order_by('-request_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Approved Requests (Ready for Delivery)"
        return context
    
@login_required
@user_passes_test(is_supplier_manager)
def cancel_delivery_action(request, pk):
     customer_request = get_object_or_404(CustomerRequest, pk=pk)
     if customer_request.status == 'delivered':
         # Logic to potentially revert stock (find the corresponding transaction and delete it, or create a 'return' transaction)
         # This can be complex and depends on your exact requirements.
         # For simplicity, maybe just change status back to 'approved'?
         customer_request.status = 'approved' # Or 'rejected' if cancelling means rejecting
         customer_request.rejection_reason = request.POST.get('reason', 'Delivery cancelled by manager.') # Get reason if provided
         customer_request.performed_by = request.user
         customer_request.save()
         messages.warning(request, f"Delivery for Request ID {customer_request.pk} cancelled.")
         # Add logic here to handle stock adjustment if needed (e.g., create a 'supply_in' transaction)
     else:
         messages.error(request, "Only delivered requests can have their delivery cancelled.")
     return redirect('supply:request_all_list') # Adjust redirect
 
 #endregion ######### Customer Request Views ###################




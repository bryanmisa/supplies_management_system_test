from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from supply.models import SupplyItem # Import from supply
from supply.views import CustomerAccessMixin # Import from supply.views if needed
from customer.models import CustomerRequest
from customer.forms import CustomerRegistrationForm, CustomerRequestForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from customer.forms import UserProfileForm


import logging
from django.http import HttpResponseRedirect

logger = logging.getLogger(__name__)

# Customer Registration
class CustomerRegistrationView(CreateView):
    form_class = CustomerRegistrationForm
    template_name = 'customer/registration/register.html' # New template
    success_url = reverse_lazy('customer:login') # Redirect to login after successful registration

    def form_valid(self, form):
        messages.success(self.request, "Registration successful! Please log in.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Registration failed. Please correct the errors below.")
        return super().form_invalid(form)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('customer:edit_profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'customer/edit_profile.html', {'form': form, 'user': request.user})
# customer/views.py

# Customer Login View

class CustomerLoginView(auth_views.LoginView):
    template_name = 'customer/registration/login.html' # New template
    redirect_authenticated_user = True # Redirect if already logged in
    
    def get(self, request, *args, **kwargs):
        logger.info(f"User: {request.user}, Authenticated: {request.user.is_authenticated}")
        return super().get(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('customer:available_supplies') # Redirect to available supplies page after login

    

# View available supplies (Customers can browse)
class AvailableSupplyListView(CustomerAccessMixin, ListView ):
    model = SupplyItem
    template_name = 'customer/available_supply_list.html' # Moved template
    context_object_name = 'available_supplies'
    paginate_by = 20 # Optional pagination

    def get_queryset(self):
        # Show active items with stock > 0
        return SupplyItem.objects.filter(status='active', quantity_in_stock__gt=0).order_by('item_name')


# Create a new request
class CustomerRequestCreateView(CustomerAccessMixin, CreateView):
    model = CustomerRequest
    form_class = CustomerRequestForm
    template_name = 'customer/customer_request_form.html' # Moved template
    # Redirect to the list of *their* requests after creation
    success_url = reverse_lazy('customer:my_requests_list')

    def form_valid(self, form):
        # Assign the logged-in user as the customer
        form.instance.customer = self.request.user
        messages.success(self.request, f"Your request for '{form.instance.supply_item.item_name}' has been submitted.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Request Supply Item"
        return context


# List the logged-in customer's own requests
class MyRequestsListView(CustomerAccessMixin, ListView):
    model = CustomerRequest
    template_name = 'customer/my_request_list.html' # New template
    context_object_name = 'customer_requests'
    paginate_by = 15 # Optional pagination

    def get_queryset(self):
        # Filter requests belonging to the currently logged-in user
        return CustomerRequest.objects.filter(customer=self.request.user).order_by('-request_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "My Supply Requests"
        return context

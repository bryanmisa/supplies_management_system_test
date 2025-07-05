# customer/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import CustomerRequest
from django.contrib.auth.models import Group # Import Group for user groups
from supply.models import SupplyItem # Import from supply
from django.contrib.auth import get_user_model

User = get_user_model() # Get the custom User model

class CustomerRegistrationForm(UserCreationForm):
    # Add any extra fields you want during registration that are on your User model
    # For example: first_name, last_name, contact_number, address
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True) # Ensure email is required
    contact_number = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        # Include username, password fields from UserCreationForm PLUS your custom fields
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'contact_number', 'address')

    def save(self, commit=True):
        user = super().save(commit=False)
        # Set the user_type specifically for customer registration
        user.user_type = 'customer'
        # Set other fields from the form
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.contact_number = self.cleaned_data.get('contact_number')
        user.address = self.cleaned_data.get('address')
        if commit:
            user.save()
            # --- Add user to the 'Customer' group ---
            try:
                customer_group = Group.objects.get(name='Customer')
                user.groups.add(customer_group)
            except Group.DoesNotExist:
                # Handle case where group doesn't exist (log error, etc.)
                print("Warning: 'Customer' group does not exist. Please create it in the admin.")
        return user

class CustomerRequestForm(forms.ModelForm):
    class Meta:
        model = CustomerRequest
        # Only fields the customer should fill
        fields = ['supply_item', 'requested_quantity']
        widgets = {
            # Consider using a Select2 widget if you have many items
            'supply_item': forms.Select(attrs={'class': 'form-control'}),
            'requested_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optionally filter the queryset for supply_item
        self.fields['supply_item'].queryset = SupplyItem.objects.filter(status='active', quantity_in_stock__gt=0)

    def clean_requested_quantity(self):
        quantity = self.cleaned_data.get('requested_quantity')
        supply_item = self.cleaned_data.get('supply_item')

        if quantity is None or quantity <= 0:
            raise forms.ValidationError("Requested quantity must be greater than zero.")

        # Optional: Check against available stock during form validation
        # if supply_item and quantity > supply_item.quantity_in_stock:
        #     raise forms.ValidationError(f"Only {supply_item.quantity_in_stock} units of {supply_item.item_name} available.")

        return quantity

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'address']

class RejectionReasonForm(forms.ModelForm):
    class Meta:
        model = CustomerRequest
        fields = ['rejection_reason']
        widgets = {
            'rejection_reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter reason for rejection'}),
        }


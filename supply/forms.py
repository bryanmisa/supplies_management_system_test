from django import forms
from supply.widgets import *
from supply.models import *
from customer.models import CustomerRequest


# Class Forms

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_email', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class SupplyItemForm(forms.ModelForm):
    class Meta:
        model = SupplyItem
        fields = [
            'item_name', 'item_code', 'category', 'description', 'quantity_in_stock',
            'reorder_level', 'unit_of_measure', 'location', 'unit_price', 'currency',
            'supplier', 'last_purchase_date', 'last_supplier_price', 'preferred_supplier',
            'status', 'barcode', 'image', 'expiration_date', 'tags'
        ]
        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'item_code': forms.TextInput(attrs={'class': 'form-control'}),
            'category': CategorySelect2Widget,
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'quantity_in_stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'reorder_level': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'unit_of_measure': forms.TextInput(attrs={'class': 'form-control'}),
            'currency': forms.TextInput(attrs={'class': 'form-control'}),
            'supplier': SupplierItemSelect2Widget,
            'last_purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'last_supplier_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'barcode': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
        }


    def clean_quantity_in_stock(self):
        quantity = self.cleaned_data.get('quantity_in_stock')
        if quantity < 0:
            raise forms.ValidationError("Quantity in stock cannot be negative.")
        return quantity

    def clean_reorder_level(self):
        reorder_level = self.cleaned_data.get('reorder_level')
        if reorder_level < 0:
            raise forms.ValidationError("Reorder level cannot be negative.")
        return reorder_level

    def clean_unit_price(self):
        unit_price = self.cleaned_data.get('unit_price')
        if unit_price < 0:
            raise forms.ValidationError("Unit price cannot be negative.")
        return unit_price
    
class SupplyTransactionForm(forms.ModelForm):
    class Meta:
        model = SupplyTransaction
        fields = [
            'supply_item', 'transaction_type', 'quantity', 'performed_by', 'remarks',
            'reference_number', 'source_location', 'destination_location'
        ]
        widgets = {
            'supply_item': SupplyItemSelect2Widget,
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'performed_by': forms.Select(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'reference_number': forms.TextInput(attrs={'class': 'form-control'}),
            'source_location': forms.TextInput(attrs={'class': 'form-control'}),
            'destination_location': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        
class RejectionReasonForm(forms.ModelForm):
    class Meta:
        model = CustomerRequest
        fields = ['rejection_reason']  # Ensure this field is included
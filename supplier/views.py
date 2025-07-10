# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from supplier.forms import SupplierRegistrationForm, SupplierLoginForm

def supplier_register(request):
    if request.method == 'POST':
        form = SupplierRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('supplier:supplier_login')
    else:
        form = SupplierRegistrationForm()
    return render(request, 'supplier/supplier_register.html', {'form': form})

def supplier_login(request):
    if request.user.is_authenticated:
        return redirect('supplier:supplier_dashboard')
    if request.method == 'POST':
        form = SupplierLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('supplier:supplier_dashboard')
    else:
        form = SupplierLoginForm()
    return render(request, 'supplier/supplier_login.html', {'form': form})

def supplier_dashboard(request):
    return render(request, 'supplier/supplier_dashboard.html')
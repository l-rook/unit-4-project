from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages, auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import RegisterForm, ProductForm, OrderForm
from .models import Prod, Order

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_user(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('login')

def product_list(request):
    products = Prod.objects.all()
    return render(request, 'product_list.html', {'products': products})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.creator = request.user  # Set creator as the logged-in user
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Prod, id=product_id)
    if product.creator != request.user:
        messages.error(request, "You don't have permission to edit this product.")
        return redirect('product_list')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Prod, id=product_id)
    if product.creator != request.user:
        messages.error(request, "You don't have permission to delete this product.")
    else:
        product.delete()
    return redirect('product_list')

def order_success(request):
    return render(request, 'order_success.html')

@login_required
def place_order(request, product_id):
    # Get the product being ordered
    product = get_object_or_404(Prod, id=product_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Create the order with the form data
            order = form.save(commit=False)
            order.product = product
            order.customer = request.user  # Link the order to the logged-in user
            order.save()
            return redirect('order_success')
    else:
        # Display the form with an initial quantity of 1
        form = OrderForm(initial={'quantity': 1})

    return render(request, 'place_order.html', {'form': form, 'product': product})


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Prod, pk=pk)
    is_creator = product.creator == request.user
    
    return render(request, 'product_detail.html', {'product': product, 'is_creator': is_creator})

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Prod, id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=product.id)
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form, 'product': product})

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Prod, pk=pk)
    if product.creator == request.user:
        product.delete()
        return redirect('product_list')  # Redirect to the product list page
    else:
        return HttpResponseForbidden("You are not authorized to delete this product.")

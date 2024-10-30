from .models import Product, Category, Cart, OrderItem, Order
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm, SellerForm, LoginForm, OrderForm
from .models import User
from django.http import JsonResponse
import json
from django.contrib.auth import logout
from decimal import Decimal

@login_required
def order(request):
    user = request.user
    categories = Category.objects.all()
    return render(request, 'shop/order.html', {'user': user, 'categories': categories})

@login_required
def order_form(request):
    if request.method == 'POST':
        body_data = request.body.decode('utf-8')
        print("Received request body in order_form:", body_data)

        try:
            items = Cart.objects.filter(user=request.user)
            if not items.exists():
                return JsonResponse({'status': 'error', 'message': 'Кошик порожній.'})

            data = json.loads(body_data) if body_data else {}
            address = data.get('shipping_address')
            postal_code = data.get('city_postal_code')
            order = Order(user=request.user, shipping_address=address, city_postal_code=postal_code)
            order.save()

            total_price = Decimal('0.00')
            for item in items:
                order_item = OrderItem(order=order, product=item.product, quantity=item.quantity, price=item.price)
                order_item.save()
                total_price += item.price * Decimal(item.quantity)

            order.total_price = total_price
            order.save()
            items.delete()

            return JsonResponse({'status': 'success', 'message': 'The order has been successfully placed.'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid data format.'})
    return render(request, 'shop/success.html')

def shopping_cart(request):
    categories = Category.objects.all()

    cart_items = []
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)

    available_stock = {item.product.id: item.product.quantity for item in cart_items}

    return render(request, 'shop/shopping_cart.html', {
        'categories': categories,
        'cart_items': cart_items,
        'available_stock': available_stock,
    })

def add_to_cart(request):
    if request.method == "POST" and request.user.is_authenticated:
        data = json.loads(request.body)
        product_id = data.get('product_id')

        product = get_object_or_404(Product, id=product_id)

        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': 1, 'price': product.price}
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return JsonResponse({'status': 'success', 'message': 'Product added to cart'})

    return JsonResponse({'status': 'error', 'message': 'Something went wrong'})

def remove_from_cart(request):
    if request.method == "POST" and request.user.is_authenticated:
        data = json.loads(request.body)
        product_id = data.get('product_id')

        cart_item = get_object_or_404(Cart, user=request.user, product_id=product_id)

        cart_item.delete()

        return JsonResponse({'status': 'success', 'message': 'Product removed from cart'})

    return JsonResponse({'status': 'error', 'message': 'Something went wrong'})

@login_required
def account(request):
    categories = Category.objects.all()
    user = request.user
    return render(request, 'shop/account.html', {'user': user, 'categories': categories})

def user_logout(request):
    logout(request)
    messages.success(request, "You are logged out!")
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
            )
            messages.success(request, "Registration is successful! You can enter.")
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'shop/registr.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are logged in!")
            return redirect('home')
        else:
            messages.error(request, "Incorrect login or password.")
    form = LoginForm()
    return render(request, 'shop/logo.html', {'form': form})

def home(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'shop/home.html', {'products': products, 'categories': categories, 'cart_items': cart_items})

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'shop/category.html', {'category': category, 'products': products, 'categories': categories})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()
    return render(request, 'shop/product_detail.html', {'product': product, 'categories': categories})

def about_us(request):
    categories = Category.objects.all()
    return render(request, 'shop/about_us.html', {'categories': categories})

def from_sellers(request):
    if request.method == 'POST':
        form = SellerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = SellerForm()
    categories = Category.objects.all()
    return render(request, 'shop/from_sellers.html', {'categories': categories, 'form': form})

def success_view(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'shop/home.html', {'products': products, 'categories': categories})




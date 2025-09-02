# store/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Q
from .models import Product, Category, Order

def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'home.html', {'products': products, 'categories': categories})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', {})
    cart[str(pk)] = cart.get(str(pk), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')

def remove_from_cart(request, pk):
    cart = request.session.get('cart', {})
    if str(pk) in cart:
        del cart[str(pk)]
    request.session['cart'] = cart
    return redirect('cart')

def update_cart(request, pk):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 0))
        cart = request.session.get('cart', {})
        if quantity > 0:
            cart[str(pk)] = quantity
        else:
            if str(pk) in cart:
                del cart[str(pk)]
        request.session['cart'] = cart
    return redirect('cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for pk, qty in cart.items():
        try:
            product = Product.objects.get(id=pk)
            item_total = product.price * qty
            total += item_total
            items.append({'product': product, 'quantity': qty, 'item_total': item_total})
        except Product.DoesNotExist:
            pass  # Remove invalid items if needed
    return render(request, 'cart.html', {'items': items, 'total': total})

def checkout(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('home')
        orders = []
        for pk, qty in cart.items():
            try:
                product = Product.objects.get(id=pk)
                order = Order.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    email=request.POST.get('email', ''),
                    address=request.POST.get('address', ''),
                    product=product,
                    quantity=qty,
                    status='Pending'
                )
                orders.append(order)
            except Product.DoesNotExist:
                pass
        del request.session['cart']
        if request.user.is_authenticated:
            return redirect('user_orders')
        else:
            request.session['recent_orders'] = [order.id for order in orders]  # For guest to view
            return redirect('purchase_complete')
    return render(request, 'checkout.html')

def purchase_complete(request):
    order_ids = request.session.get('recent_orders', [])
    del request.session['recent_orders']  # Clear after display
    orders = Order.objects.filter(id__in=order_ids)
    return render(request, 'purchase_complete.html', {'orders': orders})

def search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query) if query else Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'home.html', {'products': products, 'categories': categories})

def category_filter(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'home.html', {'products': products, 'categories': categories})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_orders(request):
    if not request.user.is_authenticated:
        return redirect('login')
    orders = Order.objects.filter(user=request.user)
    return render(request, 'user_orders.html', {'orders': orders})
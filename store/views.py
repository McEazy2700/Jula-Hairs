from datetime import datetime
import json
from django.http import JsonResponse
from django.shortcuts import render
from .models import Customer, Order, OrderItem, Product

# Create your views here.


def homePage(request):

    context = {}
    return render(request, 'store/home.html', context)


def store(request):
    search = request.GET.get('search')

    if search and search != '':
        products = Product.objects.filter(name__icontains=search)
    else:
        products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'store/store.html', context)


def cart(request):
    cookie = request.COOKIES['cart']
    cart = json.loads(cookie)
    if cart['orderId'] == 'none':
        order_id = datetime.now().timestamp()
    else: 
        order_id = cart['orderId']
    order, created = Order.objects.get_or_create(transaction_id=order_id)

    for key in cart.keys():
        if key != 'orderId':
            key_id = int(key)
            product = Product.objects.get(id=key_id)
            quantity = cart[key]['quantity']
            
        item, created = OrderItem.objects.get_or_create(order=order, product=product)
        item.quantity = quantity
        item.save()

    order.save()
       

    order_items = order.orderitem_set.all()
    context = {
        'order': order,
        'items': order_items
        }
    return render(request, 'store/cart.html', context)


def checkout(request):

    context = {}
    return render(request, 'store/checkout.html', context)


def processOrder(request):
    data = json.loads(request.body)
    form = data['form_data']
    order_id = data['orderId']
    try:
        customer = Customer.objects.get(email=form['email'])
    except:
        customer = Customer.objects.create(
            first_name=form['first_name'],
            last_name=form['last_name'],
            email=form['email'],
            phone=form['phone'])

        if customer.is_valid():
            customer.save()

    
    order = Order.objects.get(transaction_id=order_id)
    order.customer = customer
    order.complete = True
    order.save()
    return JsonResponse({'status': 'success'})
from datetime import datetime
import json
from django.http import JsonResponse
from django.shortcuts import render

from store.utils import updateDataBase
from .models import Customer, Order, OrderItem, Product

# Create your views here.


def homePage(request):

    context = {}
    return render(request, 'store/home.html', context)


def store(request):
    search = request.GET.get('search')

    if search and search != '':
        products = Product.objects.filter(name__icontains=search).order_by('-date_added')
    else:
        products = Product.objects.all().order_by('-date_added')
    context = {
        'products': products
    }
    return render(request, 'store/store.html', context)


def cart(request):
    order = updateDataBase(request)
    
       
    if order != '':
        order_items = order.orderitem_set.all()
    else:
        order_items = None
    context = {
        'order': order,
        'items': order_items
        }
    return render(request, 'store/cart.html', context)


def checkout(request):

    order = updateDataBase(request)
    
       

    if order != '':
        order_items = order.orderitem_set.all()
    else:
        order_items = None
    context = {
        'order': order,
        'items': order_items
        }
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
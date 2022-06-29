from datetime import datetime
import json
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator

from store.utils import initiatePayment, updateDataBase
from .models import Customer, Order, OrderItem, Payment, Product, Service, Testimonial

# Create your views here.


def homePage(request):

    services = Service.objects.all().order_by('-date_added')
    testimonials = Testimonial.objects.all().order_by('-date_added')

    context = {
        'services': services,
        'testimonials': testimonials
    }
    return render(request, 'store/home.html', context)


def store(request):
    search = request.GET.get('search')

    if search and search != '':
        products = Product.objects.filter(name__icontains=search).order_by('-date_added')
    else:
        products = Product.objects.all().order_by('-date_added')

    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if page_obj.paginator.num_pages > 20:
        is_paginated = True
    else:
        is_paginated = False
    context = {
        'products': products,
        'page_obj': page_obj,
        'is_paginated': is_paginated
    }

    return render(request, 'store/store.html', context)


def cart(request):
    order = updateDataBase(request)
    
       
    if order != None:
        order_items = order.orderitem_set.all()
    else:
        order_items = None
    context = {
        'order': order,
        'items': order_items
        }
    return render(request, 'store/cart.html', context)


def productDetail(request, id):
    try:
        product = Product.objects.get(id=id)
    except:
        product = None

    context = {'product': product}

    return render(request, 'store/product_detail.html', context)


def checkout(request):

    order = updateDataBase(request)
    
    

    if order != None:
        order_items = order.orderitem_set.all()
    else:
        order_items = None
    context = {
        'order': order,
        'items': order_items,
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY
        }
    
    initiatePayment(order)
    return render(request, 'store/checkout.html', context)


def processOrder(request, ref:str):
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

    try:
        payment = Payment.objects.get(ref=ref)
        payment.amount = order.getTotalPrice()
        payment.email=customer.email
        payment.customer=customer
        payment.order=order
        payment.save()
    except:
        payment = Payment.objects.create(
            ref=ref,
            amount=order.getTotalPrice(),
            email=customer.email,
            customer=customer,
            order=order
        )
        payment.save()
    verified = payment.verify_payment()
    if verified:
        pass

    order.customer = customer
    order.complete = True
    order.save()
    return JsonResponse({'status': 'success'})
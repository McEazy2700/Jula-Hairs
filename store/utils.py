import secrets
from .models import Customer, Order, OrderItem, Payment, Product
import json


def updateDataBase(request):
    try:
        cookie = request.COOKIES['cart']
        cart = json.loads(cookie)
    except:
        cookie = None
    try:
        if cart['orderId'] == 'none':
            print(cart['orderId'])
            order_id = secrets.token_urlsafe(40)
        else: 
            order_id = cart['orderId']
        order, created = Order.objects.get_or_create(transaction_id=order_id, complete=False)

        for key in cart.keys():
            if key != 'orderId':
                key_id = int(key)
                product = Product.objects.get(id=key_id)
                quantity = cart[key]['quantity']
                
            item, created = OrderItem.objects.get_or_create(order=order, product=product)
            item.quantity = quantity
            item.save()

        order.save()
        return order
    except:
        order = None
    return order


def initiatePayment(order):
    ref = order.transaction_id
    try:
        payment = Payment.objects.get(ref=ref)
    except:
        payment = Payment.objects.create(ref=ref, order=order)
    payment.save()
    return payment
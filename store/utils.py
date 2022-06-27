from .models import Customer, Order, OrderItem, Product
from datetime import datetime
import json


def updateDataBase(request):
    cookie = request.COOKIES['cart']
    cart = json.loads(cookie)
    try:
        if cart['orderId'] == 'none':
            order_id = datetime.now().timestamp()
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
    except:
        order = ''
    return order
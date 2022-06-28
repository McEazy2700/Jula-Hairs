import math
import secrets
from django.db import models
from .paystack import PayStack

# Create your models here.


class Customer(models.Model):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Product(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    in_stock = models.BooleanField(default=True)
    image = models.ImageField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name


    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = '/static/images/placeholder.jpg'
        return url


class Order(models.Model):
    transaction_id = models.CharField(max_length=200, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    complete = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        try:
            order = self.transaction_id
        except:
            order = self.id
        return str(order)

    def getTotalPrice(self):
        total = 0
        for item in self.orderitem_set.all():
            price = item.product.price * item.quantity
            total += price
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.product.name


class ShippingInfo(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.TextField(max_length=500, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        return self.address


class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ref = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return f'User:{self.email} Payment: {self.amount}'


    def amount_value(self) -> int:
        return int(math.floor(self.amount * 100))

    def verify_payment(self):
        paystack = PayStack()
        try:
            status, result = paystack.verify_payment(self.ref, self.amount)
            if status:
                if result['amount'] / 100 == self.amount:
                    self.verified = True
                self.save()
                if self.verified:
                    return True
                return False
        except:
            return False


class Testimonial(models.Model):
    image = models.ImageField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    testimony = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.testimony

    
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = '/static/images/placeholder.jpg'
        return url


class Service(models.Model):
    service_name = models.CharField(max_length=60, null=True, blank=True)
    service_image = models.ImageField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    service_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.service_name
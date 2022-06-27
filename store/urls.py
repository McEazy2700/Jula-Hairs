from django.urls import path
from .views import cart, checkout, homePage, processOrder, store


urlpatterns = [
    path('', homePage, name='homepage'),
    path('store/', store, name='store'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('process_order/', processOrder, name='process_order')
]

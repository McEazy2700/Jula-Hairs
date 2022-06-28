from django.urls import path
from .views import cart, checkout, homePage, processOrder, productDetail, store


urlpatterns = [
    path('', homePage, name='homepage'),
    path('store/', store, name='store'),
    path('store/product/<int:id>/', productDetail, name='detail'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('process_order/', processOrder, name='process_order')
]

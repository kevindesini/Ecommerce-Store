from django.urls import path
from . import views


urlpatterns = [

path('cart',views.cart,name='cart'),
path('add_cart/<product_id>/', views.add_cart, name='add_cart'),
path('inc_cart/<product_id>/<cart_item_id>/',views.inc_cart, name='inc_cart'),
path('remove_cart/<product_id>/<cart_item_id>/',views.remove_cart, name='remove_cart'),
path('remove_cart_item/<product_id>/<cart_item_id>/',views.remove_cart_item, name='remove_cart_item'),
path('checkout/', views.checkout, name='checkout'),

]
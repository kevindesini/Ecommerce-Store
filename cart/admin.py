from django.contrib import admin

# Register your models here.


from . models import CartItem, Cart

admin.site.register(CartItem)
admin.site.register(Cart)

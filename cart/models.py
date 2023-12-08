from django.db import models
from adminside.models import *
from ecommerce.models import *

# Create your models here.

class Cart(models.Model):

    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    # def __str__(self):
    #     return self.cart_id



class CartItem(models.Model):
    currentuser = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ForeignKey(SizeVariant, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
   

    def sub_total(self):
        return self.quantity * (self.product.price)

    def __str__(self):
        return self.product.product_name
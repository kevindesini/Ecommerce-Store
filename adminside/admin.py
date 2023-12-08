from django.contrib import admin
from .models import Category
from .models import Product
# Register your models here.
from . models import *

class ProductAdmin(admin.ModelAdmin):
    list_display=('product_name','price','stock','category','modified_date','is_available')
    prepopulated_fields={'slug':{'product_name',}}


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ColorVariant)
admin.site.register(SizeVariant)
admin.site.register(ImageStock)

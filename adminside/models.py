from django.db import models

# Create your models here.


class Category(models.Model):

    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    is_available = models.BooleanField(default=True)
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

def __str__(self):
        return self.category_name


class Product(models.Model):

    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # offerprice = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    images = models.ImageField(upload_to='photos/products',blank=True, null=True)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name


class ColorVariant(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return str(f'{self.product_id} ,{self.color}')


class SizeVariant(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    Color_id = models.ForeignKey(ColorVariant, on_delete=models.CASCADE)
    size = models.CharField(max_length=50)
    price = models.IntegerField()
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'id = {self.id} {self.Color_id}, {self.size}, {self.price}, {self.stock}'


class ImageStock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)
    color_variant = models.ForeignKey(ColorVariant, on_delete=models.CASCADE)
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image_stocks/')

    def __str__(self):
        return f"{self.color_variant.color} - {self.size_variant.size} Image"

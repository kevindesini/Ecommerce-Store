from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from adminside.models import *
from datetime import date
# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, user_name, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not user_name:
            raise ValueError('User must have a username')

        user = self.model(
            email=self.normalize_email(email),
            user_name=user_name,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, user_name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            user_name=user_name,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    

    # required
    profilepic = models.ImageField(upload_to='photos/profilepic')
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name', 'last_name']

    objects=MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class Userprofile(models.Model):
    currentuser = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=False)
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    is_blocked = models.BooleanField(default=False)
    homeaddress = models.TextField(default='')
    city = models.CharField(max_length=50, default='')
    pincode = models.IntegerField(default=0)
    is_default = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.currentuser}  {self.homeaddress}'s Address"
    def save(self, *args, **kwargs):
        if self.is_default:
            # Set is_default=False for other addresses of the same user
            Userprofile.objects.filter(currentuser=self.currentuser).exclude(
                pk=self.pk).update(is_default=False)
        super(Userprofile, self).save(*args, **kwargs)


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('Pending','Pending'),
    )

    user_profile = models.ForeignKey(Userprofile, on_delete=models.SET_NULL, null=True)
    # payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=200)
    address_line_2 = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)    
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    final_price = models.FloatField(blank=True,null=True)
    # discount_price=models.FloatField()
    # tax = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def full_name(self):
            return f'{self.firstname} {self.lastname}'

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'
    
    def full_address_d(self):
        return f'{self.address_line_1}, {self.address_line_2}, {self.city}, {self.state}, {self.country}'

    def __str__(self):
        return self.first_name
    

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    # payment = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True)
    user_profile = models.ForeignKey(Userprofile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ForeignKey(SizeVariant, on_delete=models.CASCADE, blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order.first_name


class Coupon(models.Model):
    coupon_code = models.CharField(max_length=20, unique=True)
    expiration_date = models.DateField(blank=False)
    discount_price = models.IntegerField(default=100)
    minimum_purchase_amount = models.IntegerField(default=500)
    

    def expiry_date(self):
        return str(self.expiration_date)

    def check_expiry(self):
        if self.expiration_date < date.today():
            return str("Expired")
        else:
            return str("Valid")

    def __str__(self):
        return self.coupon_code

class AppliedCoupon(models.Model):
    currentuser = models.ForeignKey(Account, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.coupon.coupon_code}'

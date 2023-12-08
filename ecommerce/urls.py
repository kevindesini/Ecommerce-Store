from django.contrib import admin
from .import views
from django.urls import path, include


urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.handlesignup, name='handlesignup'),
    path('resend_otp/', views.resend_otp, name='resend_otp'),
    path('login', views.handlelogin, name='handlelogin'),
    path('resend_loginotp/', views.resend_loginotp, name='resend_otp'),
    path('logout', views.handlelogout, name='handlelogout'),
    path('otp', views.otp, name='otp'),
    path('loginotp', views.loginotp, name='loginotp'),
    path('shop', views.shop, name='shop'),
    path('productdetails/<product_id>/', views.productdetails,name="productdetails"),
    path('profile', views.profile, name='profile'),
    path('editprofile', views.editprofile, name='editprofile'),
    path('saveprofile', views.saveprofile, name='saveprofile'),
    path('address', views.address, name='address'),
    path('addaddress', views.addaddress, name='addaddress'),
    path('submitaddress', views.submitaddress, name='submitaddress'),
    path('selectaddress/<int:id>',views.selectaddress,name='selectaddress'),
    path('deleteaddress/<id>',views.deleteaddress,name='deleteaddress'),
    path('editaddress/<id>/',views.editaddress, name='editaddress'),
    path('change_password', views.change_password, name='change_password'),
    path('place_order',views.place_order, name='place_order'),
    path('cashondelivery/<order_id>/',
         views.cashondelivery, name="cashondelivery"),
    path('myorders', views.myorders, name='myorders'),
    path('cancel_order/<order_id>', views.cancel_order, name='cancel_order'),
    path('order_details/<order_id>', views.order_details, name='order_details'),

    # path('profilepic', views.profilepic, name='profilepic'),

]

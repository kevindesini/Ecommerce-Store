from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import views
from django.conf import settings

urlpatterns = [
    path('adminsignin', views.adminsignin, name='adminsignin'),
    path('adminotp', views.adminsigninotp, name='adminsignin'),
    path('adminsignout', views.adminsignout, name='adminsignout'),
    path('admindashboard', views.admindashboard, name='admindashboard'),
    path('usermanagement', views.usermanagement, name='usermanagement'),
    path('blockuser/<user_id>/', views.blockuser, name='blockuser'),
    path('unblockuser/<user_id>/', views.unblockuser, name='unblockuser'),
    path('categorymanagement', views.categorymanagement, name='categorymanagement'),
    path('addcategory', views.addcategory, name='addcategory'),
    path('deactivatecategory/<category_id>/',views.deactivatecategory,name='deactivatecategory'),
    path('activatecategory/<category_id>/',views.activatecategory,name='activatecategory'),
    path('editcategory/<category_id>/', views.editcategory, name='editcategory'),
    path('productmanagement', views.productmanagement, name='productmanagement'),
    path('addproduct', views.addproduct, name='addcategory'),
    path('editproduct/<product_id>/', views.editproduct, name='editproduct'),
    path('activateproduct/<product_id>/',views.activateproduct, name='activateproduct'),
    path('deactivateproduct/<product_id>/',views.deactivateproduct, name='deactivateproduct'),
    path('variants/<product_id>/', views.variants, name='variants'),
    path('addvariants/<product_id>/', views.addvariants, name='addvariants'),
    path('editvariants/<size_id>/<product_id>/', views.editvariants, name='editvariants'),
    path('deletevariants/<product_id>/<size_id>/',
         views.deletevariants, name='deletevariants'),
    path('ordermanagement', views.ordermanagement, name='ordermanagement'),
    path('admin_change_order_status/<order_id>/', views.admin_change_order_status, name='admin_change_order_status'),
    path('orderlist/<order_id>/',
         views.orderlist, name='orderlist'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
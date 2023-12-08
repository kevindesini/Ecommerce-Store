from django.shortcuts import get_object_or_404
from django.shortcuts import render,redirect
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout
from ecommerce.models import Account
from django.core.paginator import Paginator
from django.http import HttpResponse
from adminside.models import Category
from django.utils.text import slugify
from adminside.models import Product
from django.core.mail import send_mail
import random
from adminside.models import *
from cart.models import *

# Create your views here.


def adminsignin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email = email , password = password)

        if user is not None and user.is_admin == True:
            auth.login(request, user)

            randomotp = str(random.randint(1000, 9999))
            request.session['storedotp'] = randomotp
            request.session.modified = True 
            request.session.set_expiry(300)

            subject = "OTP"
            sendermail = "Shoebuddy Ecommerce Store"
            otp = f"{randomotp}"
            send_mail(subject,otp,sendermail,[email])
        
            context = {
            'email':email
          }           
            return render(request,'admintemplates/adminsigninotp.html',context)
        
        else:
            messages.error(request,'Bad Credentials!')
            return render(request,'admintemplates/adminsignin.html')    

        


   

    return render(request,'admintemplates/adminsignin.html')
    

def adminsigninotp(request):
    if request.method == "POST":
        otp = request.POST.get('enteredotp')
        email = request.POST.get('email')
        storedotp = request.session['storedotp']

        if otp == storedotp:
            user = Account.objects.get(email=email)
            user.is_active = True
            user.save()
            messages.success(request, 'Admin is Successfully Logged in ')
            return redirect('admindashboard')
        else:
            messages.error(request, 'Wrong Entry')

            context = {
                'email': email
                
            }
            return render(request, 'adminsigninotp.html', context)
            

    return render(request, 'admintemplates/adminsigninotp.html')


def adminsignout(request):
        request.session.clear()
        logout(request)
        messages.success(request, " Admin is Logged Out Successfully")
        return render(request,'admintemplates/adminsignin.html')

def admindashboard(request):

    success_messages = messages.get_messages(request)
    context = {
        'success_messages': success_messages,
        # Other context data for your dashboard
    }


    return render(request, 'admintemplates/index.html',context)


def usermanagement(request):
    users = Account.objects.all().exclude(is_superuser=True)
    paginator = Paginator(users, 10)
    page = request.GET.get('page')
    paged_users = paginator.get_page(page)
    user_count = users.count()

    context = {
        'users': paged_users,
        'user_count': user_count
    }


    return render(request, 'admintemplates/usermanagement.html',context)


def blockuser(request,user_id):    
    # id = request.GET.get('user_id')    
    try:
        user = Account.objects.get(id=user_id)
    except Account.DoesNotExist:
        return HttpResponse("User not found")  # or return a custom response

    if request.user.is_authenticated and request.user == user:
        logout(request)
        request.session.flush()

    user.is_blocked = not user.is_blocked
    user.save()    
    messages.success(request, 'User is Blocked')
    return redirect('usermanagement')



def unblockuser(request,user_id):
    # id = request.GET.get('usr_id')
    try:
        user = Account.objects.get(id=user_id)
    except Account.DoesNotExist:
        return HttpResponse("User not found")  # or return a custom response

    user.is_blocked = False
    user.save()

    messages.success(request, 'User is Unblocked')
    return redirect('usermanagement')


def categorymanagement(request):
    categories = Category.objects.all().order_by('-id')
    paginator = Paginator(categories, 10)
    page = request.GET.get('page')
    paged_categories = paginator.get_page(page)
    category_count = categories.count()
    context = {
        'categories': paged_categories,
        'category_count': category_count
    }

    return render(request, 'admintemplates/categorymanagement.html',context)


def addcategory(request):
    if request.method == "POST":
        category_name = request.POST.get('category_name')
        slug          = request.POST.get('category_slug')
        description = request.POST.get('category_description')
        if not Category.objects.filter(category_name=category_name).exists():
            category = Category(
                category_name=category_name,
                slug          = slug,
                description=description
            )          

            category.save()
            return redirect('categorymanagement')
        else:
            messages.warning(request, f'A category with the name {category_name} already exists.')
            return redirect ('categorymanagement')
    return render(request, 'admintemplates/addcategory.html')


def deactivatecategory(request, category_id):
    category = Category.objects.get(id=category_id)
    category.is_available = False
    category.save()  

    return redirect('categorymanagement')


def activatecategory(request, category_id):
    category = Category.objects.get(id=category_id)
    category.is_available = True
    category.save()
    return redirect('categorymanagement')


def editcategory(request,category_id):

    if request.method == "POST":       

        categoryname = request.POST['category_name']
        categoryslug = request.POST['category_slug']
        categorydescription = request.POST['category_description']
        category_id = request.POST['category_id']
        categoryslug = slugify(categoryname)

        if not Category.objects.filter(category_name=categoryname).exclude(id=category_id).exists():

            categ = Category.objects.get(id=category_id)
            categ.category_name = categoryname
            categ.description = categorydescription
            categ.slug = categoryslug
            categ.save()
            messages.success(request, 'Successfully Saved')
            return redirect('categorymanagement')
        
        else:
            messages.warning(request, f'A category with the name {categoryname} already exists.')
            return redirect ('categorymanagement')
    else:

        # id = request.GET.get('cat_id')

        cats = Category.objects.get(id=category_id)
        context = {
            'cats': cats
        }
        return render(request, 'admintemplates/editcategory.html',context)


def productmanagement(request):
    products = Product.objects.all().order_by('-id')
    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count
    }

    return render(request, 'admintemplates/productmanagement.html',context)


def addproduct(request):
    if request.method == "POST":
        productname = request.POST['product_name']
        category_id = request.POST['category_id']
        productdescription = request.POST['product_description']
        productprice = request.POST['product_price']
        productstock = request.POST['product_stock']
        productslug        = request.POST['product_slug']
        productimage = request.FILES['product_image']
        print(type(productprice))

        category = Category.objects.get(id=category_id)
        if not Product.objects.filter(product_name=productname).exists():
   
    # ...

            product = Product(
            product_name=productname,
            category=category,
            slug         = productslug,
            description=productdescription,
            # offerprice=productprice,
            price=float(productprice),
            stock=int(productstock),
            images=productimage
        )
            product.save()
        else:
            messages.error(
                request, f'A product with the name {productname} already exists.')



        messages.success(request, 'Product Added.')
        return redirect('productmanagement')

    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'admintemplates/addproduct.html', context)


def editproduct(request, product_id):

    if request.method == "POST":

        productname = request.POST['product_name']
        productslug = slugify(productname)
        productdescription = request.POST['description']
        productprice = request.POST['price']
        productstock = request.POST['stock']
        try:
            productimages = request.FILES['images']
        except:
            pass
        productcategory = request.POST['category_id']
        productid = request.POST['product_id']

        category = Category.objects.get(id=productcategory)

        if not Product.objects.filter(product_name=productname).exclude(id=product_id).exists():
            product = Product.objects.get(id=product_id)
            product.product_name = productname
            product.slug = productslug
            product.description = productdescription
            product.stock = productstock
            product.category = category
            product.price = productprice

        

            try:
                if productimages is not None:
                    product.images = productimages
            except:
                pass
            
            product.save()
        else:
            messages.warning(request, f'A product with the name {productname} already exists.')
            return redirect ('productmanagement')
        messages.success(request, 'Successfully Saved')
        return redirect('productmanagement')

    category = Category.objects.all()

    
    pros = Product.objects.get(id=product_id)
    context = {
        'pros': pros,
        'category': category,
    }

    return render(request, 'admintemplates/editproduct.html', context)




def activateproduct(request, product_id):
    product = Product.objects.get(id=product_id)
    product.is_available = True
    product.save()
    return redirect('productmanagement')


def deactivateproduct(request, product_id):
    product = Product.objects.get(id=product_id)
    product.is_available = False
    product.save()
    return redirect('productmanagement')


def variants(request, product_id):
    product = Product.objects.get(id=product_id)
    sizes = SizeVariant.objects.filter(product_id=product, is_available=True)
    for i in sizes:
        print(i,'\n\n')
    context = {
        'sizes': sizes,
        'product': product,
    }
    return render(request, 'admintemplates/variants.html', context)


def addvariants(request, product_id):
    if request.method == 'POST':
        # Convert product_id to integer
        product_id = int(product_id)
        color = request.POST.get('color')
        size = request.POST.get('size')
        stock = request.POST.get('stock')
        price = request.POST.get('price')
        product_image=request.FILES.get('product_image')
        product = Product.objects.get(id=product_id)

        if ColorVariant.objects.filter(product_id=product_id, color=color).exists():
            color_v = ColorVariant.objects.get(
                product_id=product_id, color=color)
            size_v = SizeVariant(
                product_id=product, Color_id=color_v, size=size, stock=stock, price=price)
            size_v.save()
            image = ImageStock.objects.create(product=Product.objects.get(id=product_id), color_variant=color_v, size_variant=size_v, image=product_image
                              )
            image.save()
            return redirect('variants', product_id=product_id)
        else:
            color_v = ColorVariant(product_id=product, color=color)
            color_v.save()
            size_v = SizeVariant(
                product_id=product, Color_id=color_v, size=size, stock=stock, price=price)
            size_v.save()
            image = ImageStock.objects.create(product=Product.objects.get(id=product_id), color_variant=color_v, size_variant=size_v, image=product_image
                                              )
            image.save()
            
            return redirect('variants', product_id=product_id)

    # product_id = request.GET.get('product_id')
    product = Product.objects.get(id=product_id)
    context = {'product': product}
    return render(request, 'admintemplates/addvariants.html', context)



def editvariants(request, size_id, product_id):
    print("****", size_id)
    if request.method == 'POST':
        # product_id = request.POST.get('product_id')        
        new_color = request.POST.get('color')
        new_size = request.POST.get('size')
        stock = request.POST.get('stock')
        price = request.POST.get('price')
        product_image = request.FILES.get('product_image')
        size = SizeVariant.objects.get(id=size_id)
        color = size.Color_id
        color.color = new_color
        color.save()
        size.size = new_size
        size.price = price        
        size.stock = stock


        # -----
        image = ImageStock.objects.get(product=Product.objects.get(id=product_id))
        image.color_variant = new_color
        image.image = product_image
        image.save()
        # image = ImageStock.objects.create(product=Product.objects.get(id=product_id), color_variant=color_v, size_variant=size_v, image=product_image
        #             )
        size.save()
        return redirect('variants', product_id)
    # color = ColorVariant.objects.get()
    size = SizeVariant.objects.get(id=size_id)
    context = {'size': size, 'product_id': product_id}
    return render(request, 'admintemplates/editvariants.html', context)


# def deletevariants(request, product_id):
#     try:
#         # Assuming SizeVariant has a ForeignKey to Product with a field named product_id
#         variant = get_object_or_404(SizeVariant, id=product_id)
#         product_id = variant.product_id.id
#         variant.delete()
#         messages.warning(request, "Variant deleted successfully")
#         return redirect('variants', product_id)
#     except SizeVariant.DoesNotExist:
#         # Handle the case where the SizeVariant with the specified id does not exist
#         messages.error(request, "Variant not found")
#         return redirect('variants')  # Redirect to an appropriate page


def deletevariants(request,product_id,size_id):
    variant = SizeVariant.objects.get(id=size_id)
    variant.delete()
    messages.warning(request, "Varient deleted Successfully")
    return redirect('variants', product_id) 


def ordermanagement(request):
      
    # address = Userprofile.objects.get(currentuser=request.user,is_default=True)

    orders = Order.objects.filter(is_ordered=True).order_by('-created_at')
    context = {
        "orders": orders,
        # "address":address,
    }
    return render(request, 'admintemplates/ordermanagement.html', context)


def admin_change_order_status(request, order_id):
    order = Order.objects.get(id=order_id)
    status = request.POST.get(f'status-{order_id}')
    order.status = status
    order.save()
    context = {
        "status": status
    }
    # render(request,'admintemplates/ordermanagement.html',context)
    return redirect('ordermanagement')

def orderlist(request,order_id):
    order = Order.objects.get(id=order_id)
    order_items = OrderProduct.objects.filter(order=order)
    context = {
        "order_items": order_items
    }
    return render(request, 'admintemplates/orderlist.html',context )

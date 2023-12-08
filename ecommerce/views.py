from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login ,logout
import random
from django.core.mail import send_mail
from ecommerce.models import *
from ecommerce.models import MyAccountManager
from django.contrib import messages, auth
from adminside.models import *
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from cart.models import *
from datetime import date
import datetime


def home(request):
    category = request.GET.get('category')
    if category:
        cat = Category.objects.get(slug=category)
        products = Product.objects.filter(category=cat)
    else:
        products = Product.objects.all()

    items_per_page = 8
    paginator = Paginator(products, items_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'products': page,
    }   

    return render(request,'usertemplates/home.html',context)

def handlesignup(request):
    #   if request.user.is_authenticated:        
    #     return redirect("home")
      
      if request.method=="POST":
          firstname = request.POST.get("firstname")
          lastname = request.POST.get("lastname")
          username=request.POST.get("username")
          email=request.POST.get("email")          
          password=request.POST.get("pass1")
          confirmpassword=request.POST.get("pass2")
          if password != confirmpassword:
              messages.warning(request, "Password is Incorrect")
              return redirect('/signup')
          
          try:
              if Account.objects.get(username=username):
                 messages.info(request, "UserName is Taken")
                 return redirect('/signup')
          except:
              pass
          try:
              if Account.objects.get(email=email):
                  messages.info(request, "Email is Taken")
                  return redirect('/signup')
          except:
              pass     
                 
          myuser=Account.objects.create_user(firstname,lastname,username,email,password)
          myuser.is_admin = False
          myuser.is_active = False
          myuser.is_staff = False
          myuser.is_superuser = False
          myuser.save()

          randomotp = str(random.randint(1000, 9999))
          request.session['user_email'] = email
          request.session['storedotp'] = randomotp
          request.session['otp_expiry']=20
          request.session.modified = True 
          

          subject = "OTP"
          sendermail = "Shoebuddy Ecommerce Store"
          otp = f"{randomotp}"
          send_mail(subject,otp,sendermail,[email])
        
          context = {
            'email':email,
            'otp_expiry': request.session['otp_expiry']
          }
        # messages.success(request,'Your Account Has Been Successfully Created')
          return render(request,'usertemplates/otp.html',context)

          
      
      
      return render(request,'usertemplates/signup.html')


def otp(request):
    if request.method == "POST":
        otp = request.POST.get('enteredotp')
        email = request.POST.get('email')
        storedotp = request.session['storedotp']

        if otp == storedotp:
            user = Account.objects.get(email=email)
            user.is_active = True
            user.save()
            messages.success(request, 'User is Successfully Registered')
            return redirect('handlelogin')
        else:
            messages.error(request, 'Wrong Entry')

            context = {
                'email': email
            }
            return render(request, 'usertemplates/otp.html', context)

    return render(request, 'usertemplates/otp.html')


def resend_otp(request):
    if request.method == 'GET':
        # Generate a new OTP
        new_otp = str(random.randint(1000, 9999))
        request.session['storedotp'] = new_otp
        request.session['otp_expiry'] = 20  # Set expiry time in seconds
        request.session.modified = True

        # Resend the new OTP to the user's email
        email = request.session.get('user_email', '')
        subject = "Resent OTP"
        sendermail = "Shoebuddy Ecommerce Store"
        otp = f"{new_otp}"
        send_mail(subject, otp, sendermail, [email])

        messages.success(request, 'OTP Resent Successfully!')
        # Update with the actual URL for OTP verification
        return redirect('otp')
    else:
        # Redirect to home or any other appropriate URL
        return redirect('')

def handlelogin(request):
       if request.method=="POST":
          email=request.POST.get("email")
          password=request.POST.get("password")
          myuser=authenticate(email=email,password=password)
          
          if myuser is not None and myuser.is_admin == False and myuser.is_blocked == False:
               login(request,myuser)
               randomotp = str(random.randint(1000, 9999))
               request.session['storedotp'] = randomotp
               request.session.modified = True 
            #    request.session.set_expiry(300)

               subject = "OTP"
               sendermail = "Shoebuddy Ecommerce Store"
               otp = f"{randomotp}"
               send_mail(subject,otp,sendermail,[email])
        
               context = {
                'email':email
                 }
               return render(request, 'usertemplates/loginotp.html', context)
          
          elif myuser is not None and myuser.is_blocked:

            messages.error(request, 'Your account is blocked.')
            return render(request, 'usertemplates/login.html') 
               
          else:
                messages.error(request,"Invalid Credentials")
                return render(request, 'usertemplates/login.html')
           
       return render(request,'usertemplates/login.html')
def loginotp(request):
    if request.method == "POST":
        otp = request.POST.get('enteredotp')
        email = request.POST.get('email')
        storedotp = request.session['storedotp']

        if otp == storedotp:
            user = Account.objects.get(email=email)
            user.is_active = True
            user.save()
            messages.success(request, 'User is Successfully Logged in')
            return redirect('/')
        else:
            messages.error(request, 'Wrong Entry')

            context = {
                'email': email
            }
            return render(request, 'usertemplates/loginotp.html', context)

    return render(request, 'usertemplates/loginotp.html')


def resend_loginotp(request):
    if request.method == 'GET':
        # Generate a new OTP
        new_otp = str(random.randint(1000, 9999))
        request.session['storedotp'] = new_otp
        request.session['otp_expiry'] = 20  # Set expiry time in seconds
        request.session.modified = True

        # Resend the new OTP to the user's email
        email = request.session.get('user_email', '')
        subject = "Resent OTP"
        sendermail = "Shoebuddy Ecommerce Store"
        otp = f"{new_otp}"
        send_mail(subject, otp, sendermail, [email])

        messages.success(request, 'OTP Resent Successfully!')
        # Update with the actual URL for OTP verification
        return render(request, 'usertemplates/loginotp.html')
    else:
        # Redirect to home or any other appropriate URL
        return redirect('')






def handlelogout(request):
    logout(request)
    messages.info(request, "Logout Success ")
    return redirect('/login')


def shop(request):
    category = request.GET.get('category')
    if category:
        cat = Category.objects.get(slug=category)
        products = Product.objects.filter(category=cat)
    else:
        products = Product.objects.all().exclude(is_available=False)

    items_per_page = 9
    paginator = Paginator(products, items_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'products': page,
    }

    return render(request, 'usertemplates/shop.html', context)


def productdetails(request, product_id):
    product = Product.objects.get(id=product_id)
    products = Product.objects.filter(is_available=True)[:4]
    color = {i.Color_id for i in SizeVariant.objects.select_related(
        'Color_id').filter(is_available=True, product_id=product_id)}
    # color = ColorVariant.objects.filter(product_id=product, is_available=True)
    size3 = SizeVariant.objects.filter(product_id=product, is_available=True)    
    size_set = set()
    print(color)
    for size in size3:
        size_set.add(size.size)
    size_list = list(size_set)
    size_list.sort()

    context = {
        'products': products,
        'products1':[] ,
        'product':product,
        
        'color': color,
        'size': size3,
    }
    return render(request, 'usertemplates/productdetails.html', context)


def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    currentuser = request.user
    usr = Account.objects.get(email=currentuser)
    context = {
        'usr': usr
    }
    return render(request, 'usertemplates/profile.html',context)


# def profilepic(request):

#     image = request.FILES['product_image']
#     currentuser = Account.objects.get(email=request.user)
#     currentuser.profilepic = image
#     currentuser.save()
#     return render(request, 'usertemplates/profile.html')


def editprofile(request):

    currentuser = request.user
    usr = Account.objects.get(email=currentuser)
    context = {
        'usr': usr
    }

    return render(request, 'usertemplates/editprofile.html',context)


def saveprofile(request):
    print('********************')  
    if request.method == "POST":

        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        mobile= request.POST['mobile']
        # password=request.POST['password']
        userid= request.POST['user_id']

        usr = Account.objects.get(id=userid)

        usr.first_name = firstname
        usr.last_name = lastname
        usr.user_name = username
        usr.email = email
        usr.mobile = mobile
        # usr.password = password

        usr.save()
        messages.success(request, 'Successfully Saved Changes')

        return redirect('profile')

    return render(request, 'usertemplates/editprofile.html')

def address(request):
    
    # Assuming you have a foreign key relationship between UserAddress and Account
    current_user = request.user
    addresses = Userprofile.objects.filter(currentuser=current_user)

    context = {
        'addresses': addresses
    }

    return render(request, 'usertemplates/address.html', context)
    

def addaddress(request): 
    request.session["redirect"] = request.build_absolute_uri()

    return render(request, 'usertemplates/addaddress.html')

def submitaddress(request):
    if request.method == 'POST':
        currentuser = Account.objects.get(id=request.user.id)
        currentuser = request.user
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        mobile = request.POST['mobile']
        homeaddress = request.POST['homeaddress']
        city = request.POST['city']
        pincode = request.POST['pincode']

        address = Userprofile.objects.create(
            currentuser=currentuser,
            firstname=firstname,
            lastname=lastname,
            email=email,
            mobile=mobile,
            homeaddress=homeaddress,
            city=city,
            pincode=pincode
        )
        print("\n\n\n", request.session["redirect"])
        address.save()
        messages.success(request, 'Address successfully added')
    # return redirect('address')
    return HttpResponseRedirect(request.session["redirect"])

def selectaddress(request, id):
    address = Userprofile.objects.get(id=id)
    address.is_default = True
    address.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def deleteaddress(request, id):
    print("############################")
    
    address = Userprofile.objects.get(id=id)    
    # Check if the address is the default address
    if address.is_default:
        messages.error(request, 'Cannot delete the default address.')
    else:
        address.delete()
        messages.success(request, 'Address deleted successfully.')
        
    # return render(request, 'usertemplates/checkout.html')
    return redirect('checkout')




def editaddress(request,id):   
    
    address = Userprofile.objects.get(id=id)  
    
    print("#####################")

    if request.method == 'POST':
        # Get the form data from the request
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        homeaddress = request.POST.get('homeaddress')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')

        # Update the address fields
        address.firstname = firstname
        address.lastname = lastname
        address.email = email
        address.mobile = mobile
        address.homeaddress = homeaddress
        address.city = city
        address.pincode = pincode

        # Save the updated address
        address.save()

        # Redirect to a success page or profile page
        return redirect('checkout')

    # Render the edit address form
    return render(request, 'usertemplates/editaddress.html', {'address': address})
    # return render(request, 'usertemplates/editaddress.html')


def change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_new_password']
        user = Userprofile.objects.get(email=request.user)
        user1 = Account.objects.get(email=request.user)
        if new_password == confirm_password and user1.check_password(current_password):
            # user.check_password(current_password)
            user1.set_password(new_password)
            user1.save()

            # Update the session to avoid logout after password change
            update_session_auth_hash(request, user1)

            messages.success(request, 'Password updated successfully')
            return redirect('change_password')
        elif new_password != confirm_password:
            messages.error(request, "Passwords don't match")
        else:
            messages.error(request, 'Current Password is incorrect')   
        
            
    return render(request, 'usertemplates/changepassword.html')






def place_order(request, total=0, quantity=0,):

    current_user = request.user
    address = Userprofile.objects.get(currentuser=request.user,is_default=True)

    user_profile = Userprofile.objects.get(currentuser=current_user, is_default=True)
    print('\n\n', user_profile)
    # If the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(currentuser=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('shop')

    grand_total = 0    

    for cart_item in cart_items:
        total += (cart_item.variations.price * cart_item.quantity)
        quantity += cart_item.quantity
    
    grand_total = total
    if request.method == 'POST':
        # Extract form data from POST request
        # firstname = request.POST.get('first_name')
        # lastname = request.POST.get('last_name')
        # phone = request.POST.get('phone')
        # email = request.POST.get('email')
        # address_line_1 = request.POST.get('address_line_1')
        # address_line_2 = request.POST.get('address_line_2')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        order_note = request.POST.get('order_note')

        # user_profile = user_profile.first()
        # Store all the billing information inside Order table
        data = Order()
        data.user_profile = user_profile
        # data.firstname = firstname
        # data.lastname = lastname
        # data.phone = phone
        # data.email = email
        # data.address_line_1 = address_line_1
        # data.address_line_2 = address_line_2        
        data.country = country
        data.state = state
        data.city = city
        data.order_note = order_note
        data.order_total = grand_total       
        data.ip = request.META.get('REMOTE_ADDR')
        data.save()
        
        

        # Generate order number
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr, mt, dt)
        current_date = d.strftime("%Y%m%d")  # 20210305
        order_number = current_date + str(data.id)
        data.order_number = order_number
        data.save()
        print("##################################")
        # wallet = Wallet.objects.get(user=user)
        order = Order.objects.get(
            user_profile=user_profile, is_ordered=False, order_number=order_number)
        # user_profile= Userprofile.objects.filter(currentuser=current_user)
        
        for cart_item in cart_items:
            variation = cart_item.variations
        # Decrease variantstock by cart_item.quantity
            variation.stock -= cart_item.quantity
        # Ensure the variantstock doesn't go below 0
            variation.stock = max(variation.stock, 0)
            variation.save()


            ord = OrderProduct(order=order, user_profile=user_profile,
                               product=cart_item.product,
                               variations=cart_item.variations,
                               quantity=cart_item.quantity,
                               product_price=cart_item.variations.price*cart_item.quantity)
        
            ord.save()
        
        context = {
            'order': order,
            'cart_items': cart_items,
            'total': total,            
            'grand_total': grand_total,
            'address': address,
            # 'wallet.amount': wallet.amount,
            'discount_price': 0
        }
        return render(request, 'usertemplates/placeorder.html', context)
    else:
        return redirect('checkout')


def cashondelivery(request, order_id):
    
   
    # discount_price = request.GET.get('discount_price')
    current_user = request.user
    order = Order.objects.get(id=order_id)
    order.is_ordered = True
    order_products = OrderProduct.objects.filter(order=order)
    order_products.update(ordered=True)
    user= Userprofile.objects.get(
        currentuser=current_user, is_default=True)
    address=user
   
    
    # order.save()
    order_products = OrderProduct.objects.filter(order=order)
    for item in order_products:
       
        item.ordered = True
        item.save()
    # if discount_price:
    #     # total=order.order_total-discount_price
    #     # discount_price = float(discount_price)
    #     # order.discount_Price = discount_price
    #     # total = order.order_total - discount_price
    #     order.discount_amount = total
    #     order.save()
    # else:
        order.final_price = order.order_total
        order.save()
    cart = CartItem.objects.filter(currentuser=current_user)
    cart.delete()
    messages.success(request, 'order successfull')
    
    context = {'orders': [order],
               'address': address, }
    
    return render(request,'usertemplates/myorders.html',context)


def myorders(request):
    current_user = Account.objects.get(email=request.user)
    orders = Order.objects.filter(
        user_profile__currentuser__email=current_user, is_ordered=True
    ).order_by('-created_at')
    paginator = Paginator(orders, 11)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = orders.count()
    

    # order = Order.objects.get(user_profile=request.user, is_default=True)
    # orders = Order.objects.filter(user_id=request.user.id,is_ordered =True).order_by('-created_at')
    context = {
        'orders': paged_products,
        'product_count': product_count,
        # 'order':order

    }
    return render(request, 'usertemplates/myorders.html', context)

def cancel_order(request,order_id):
    order = Order.objects.get(id=order_id)
    order.status = "Cancelled"
    order.save()
    return redirect('myorders')


def order_details(request, order_id):
    order = Order.objects.get(id=order_id)
    order_items = OrderProduct.objects.filter(order=order)
    context = {
        "order_items": order_items
    }
    return render(request, 'usertemplates/orderdetails.html', context)

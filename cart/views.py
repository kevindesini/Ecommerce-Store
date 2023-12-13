from django.shortcuts import render , redirect, get_object_or_404
from adminside.models import *
from ecommerce.models import *
from .models import Cart, CartItem
from django.contrib import messages
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, JsonResponse
# Create your views here.


def  _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return redirect('cart')




def add_cart(request, product_id):
    if request.method == 'POST':
        color_id = request.POST.get('color_id')
        size_id = request.POST.get('size_id')
        quantity = 1
        product = Product.objects.get(id=product_id)
        color = ColorVariant.objects.get(id=color_id)
        
        if request.user.is_authenticated:
            
            try:
                variant = SizeVariant.objects.get(id=size_id, Color_id=color)
                try:
                    cart_item = CartItem.objects.get(currentuser=request.user, variations=variant)
                    if variant.stock >= quantity:
                        print("After variant\n\n")
                        # variant.stock -= 1
                        # variant.save()
                        cart_item.quantity += 1
                        cart_item.save()
                except:                  
                    
                    # if variant.stock >= quantity:
                    #     variant.stock -= 1
                    #     variant.save()
                    cart_item = CartItem.objects.create(
                        currentuser=request.user, variations=variant, quantity=quantity,product=product)
                    cart_item.save()

                messages.warning(
                    request, "Product Added to Cart.")
                return redirect('productdetails', product_id)
            except:
                messages.warning(request, "This Color does not have this Size, Please Select another.")
                return redirect('productdetails', product_id)
            
        else: 
                       
            try:
                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                except Cart.DoesNotExist:
                    cart = Cart.objects.create(cart_id=_cart_id(request))
                cart.save()
                variant = SizeVariant.objects.get(id=size_id)
                cart_item = CartItem.objects.get(cart=cart, variations=variant)
                if variant.stock >= quantity:
                        # variant.stock -= 1
                        # variant.save()
                        cart_item.quantity += 1
                        cart_item.save()
            except:                       
                    # if variant.stock >= quantity:
                    #     variant.stock -= 1
                    #     variant.save()
                        cart_item = CartItem.objects.create(
                            cart=cart, variations=variant, quantity=quantity, product=product)
                        cart_item.save()
            messages.warning(request, "Product Added to Cart with no user")
            return redirect('productdetails',product_id)   



# def add_cart(request,product_id):
#     # print("*****************", request.user)
#     if request.method == 'POST':
        
#         # product = Product.objects.get(id=product_id)
#         size_id = request.POST.get('size_id')
#         color_id = request.POST.get('color_id')
#         print("size_id = ", size_id)
#         print("color_id = ", color_id)
#         quantity = 1
#         if request.user.is_authenticated:
#             product = Product.objects.get(id=product_id)
#             color = ColorVariant.objects.get(id=color_id)
#             try:
#                 variant = SizeVariant.objects.get(id=size_id, Color_id=color)
#                 cart_item = CartItem.objects.filter(variations=variant, currentuser=request.user)
#                 print("CART ITEM",len(cart_item))

#             except:
#                 messages.warning(request, "This Color does not have this Size, Please Select another.")
#                 return redirect('productdetails', product_id)
            
#             try:
#                 cart_item = CartItem.objects.filter(variations=variant, currentuser=request.user)
#                 if len(cart_item) == 1:
#                     cart_item = CartItem.objects.get(variations=variant, currentuser=request.user)
#                     if variant.stock >= quantity:
#                         variant.stock -= quantity
#                         cart_item.quantity += quantity
#                         cart_item.save()
#                         variant.save()
#                         messages.success(request, 'Product Added to cart ')
#                         return redirect('productdetails', product_id)
#                 else:
#                     if variant.stock >= quantity:
#                         variant.stock -= quantity
#                         cart_item = CartItem(product=product, quantity=quantity,
#                                                             currentuser=request.user,
#                                                             variations=variant,
#                                                             )
#                         cart_item.save()
#                         messages.success(request, 'Product Added to cart ')
#                         return redirect('productdetails', product_id)

#                     else:
#                         messages.info(request, 'Product Out of stock ')
#                         return redirect('productdetails', product_id=product_id)

#             except CartItem.DoesNotExist:
#                 if variant.stock >= quantity:
#                     variant.stock -= quantity
#                     cart_item = CartItem.objects.create(product=product,
#                                                         quantity=quantity,
#                                                         currentuser=request.user,
#                                                         variations=variant,
#                                                         )
#                     cart_item.save()
#                 else:
#                     messages.info(request, 'Product Out of stock')
#                     return redirect('productdetails', product_id=product_id)
#                 return redirect('cart')




#         #     total_items = CartItem.objects.filter(currentuser=request.user).aggregate(total_quantity=Sum('quantity'))['total_quantity']
#         #     if total_items is None:
#         #         total_items = 0
#         #     if total_items > 10:
#         #         messages.warning(
#         #             request, f'Cart Limit Reached You already have {total_items} in Your cart and you can add {10-total_items} items')
#         #         return redirect('productdetails',product_id)
#         #     if size_id and color_id:
#         #         product = Product.objects.get(id=product_id)

#         #         color = ColorVariant.objects.get(id=color_id)
                
#         #         try:
#         #             print("***************", size_id, color_id)
#         #             variant = SizeVariant.objects.get(
#         #                 id=size_id, Color_id=color)
#         #             print("*************variant**", variant)
#         #         except:
#         #             messages.warning(
#         #                 request, "This Color does not have this Size, Please Select another.")
#         #             return redirect('productdetails', product_id)
#         #         try:
#         #             total_items = CartItem.objects.filter(currentuser=request.user).aggregate(total_quantity=Sum('quantity'))[
#         #                 'total_quantity']
#         #             if total_items is None:
#         #                 total_items = 0
#         #             if total_items + quantity > 10:
#         #                 messages.warning(request,
#         #                                  f'Cart Limit Reached You already have {total_items} items '
#         #                                  f'in Your cart and you can add {10 - total_items} items')
#         #                 return redirect('productdetails',product_id)
#         #             if CartItem.objects.filter(variations=variant, currentuser=request.user).exists():
#         #                 cart_item = CartItem.objects.get(
#         #                     variations=variant, currentuser=request.user)
#         #             else:
#         #                 cart_item = CartItem(variations=variant, currentuser=request.user, quantity=0)
#         #                 cart_item.save()
#         #             print(cart_item)
#         #             if variant.stock > quantity:
#         #                 variant.stock -= quantity
#         #                 cart_item.quantity += quantity
#         #                 cart_item.save()
#         #                 variant.save()
#         #                 messages.success(request, 'Product Added to cart ')
#         #                 return redirect('productdetails', product_id)
#         #             else:
#         #                 messages.info(request, 'Product Out of stock ')
#         #                 return redirect('productdetails', product_id=product_id)
#         #         except CartItem.DoesNotExist:
#         #             if variant.stock >= quantity:
#         #                 variant.stock -= quantity
#         #                 cart_item = CartItem.objects.create(product=product,
#         #                                                     quantity=quantity,
#         #                                                     currentuser=request.user,
#         #                                                     variations=variant,
#         #                                                     )
#         #                 cart_item.save()
#         #             else:
#         #                 messages.info(request, 'Product Out of stock')
#         #                 return redirect('productdetails', product_id=product_id)
#         #         return redirect('cart')
#         #     else:
#         #         messages.error(request, 'Please Select a Color and Size')
#         #         return redirect('productdetails', product_id=product_id)
#         else:
#             if size_id:
#                 product = Product.objects.get(id=product_id)
#                 variant = SizeVariant.objects.get(id=size_id)
#                 try:
#                     cart = Cart.objects.get(cart_id=_cart_id(request))
#                 except Cart.DoesNotExist:
#                     cart = Cart.objects.create(cart_id=_cart_id(request))
#                 cart.save()
#                 total_items = CartItem.objects.filter(cart=cart).aggregate(
#                     total_quantity=Sum('quantity'))['total_quantity']
#                 if total_items is None:
#                     total_items = 0
#                 if total_items > 10:
#                     messages.warning(request,
#                                      f'Cart Limit Reached You already have {total_items} in Your cart and you can add {10 - total_items} items')
#                     return redirect('productdetails', product_id=product_id)
#                 try:
#                     total_items = CartItem.objects.filter(cart=cart).aggregate(total_quantity=Sum('quantity'))[
#                         'total_quantity']
#                     if total_items is None:
#                         total_items = 0
#                     if total_items+quantity > 10:
#                         messages.warning(request,
#                                          f'Cart Limit Reached You already have {total_items} items '
#                                          f'in Your cart and you can add {10 - total_items} items')
#                         return redirect('productdetails', product_id=product_id)
#                     cart_item = CartItem.objects.get(
#                         variations=variant, cart=cart)
#                     if variant.stock > quantity:
#                         variant.stock -= quantity
#                         cart_item.quantity += quantity
#                         cart_item.save()
#                     else:
#                         messages.info(request, 'Product Out of stock ')
#                         return redirect('productdetails', product_id=product_id)
#                 except CartItem.DoesNotExist:
#                     if variant.stock > quantity:
#                         variant.stock -= quantity
#                         cart_item = CartItem.objects.create(product=product,
#                                                             quantity=quantity,
#                                                             cart=cart,
#                                                             variations=variant)
#                         cart_item.save()
#                     else:
#                         messages.info(request, 'Product Out of stock  ')
#                         messages.error(
#                             request, 'Please Select a Color and Size')
#             else:
#                 messages.error(request, 'Please Select a Color and Size')
#                 return redirect('productdetails', product_id=product_id)

#             messages.success(request, 'Product Added to Cart')
#             return redirect('productdetails', product_id=product_id)
    
def remove_cart(request, product_id, cart_item_id):
    # product = get_object_or_404(Product, id=product_id)
    product = Product.objects.get(id=product_id)
    print(product_id)
    try:
        if request.user.is_authenticated:          

            cart_item = CartItem.objects.get(
                product=product, currentuser=request.user, id=cart_item_id)
            cart_items = CartItem.objects.filter(currentuser=request.user)
            
        else:
            print("notlogged")
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(
                product=product, cart=cart, id=cart_item_id)
            cart_items = CartItem.objects.filter(cart=cart)
        if cart_item.quantity > 1:
            variant = cart_item.variations
            cart_item.quantity -= 1
            cart_item.save()
            # tax = 0
            # grand_total = 0
            total = 0

            for cart_itm in cart_items:
                total += (cart_itm.variations.price * cart_itm.quantity)
            # tax = (2 * total)/100
            # grand_total = total + tax
            return JsonResponse({
                'price': cart_item.variations.price,
                'total': total,
                'quantity': cart_item.quantity,
                # 'tax': tax,
                # 'grand_total': grand_total,
            })
        else:
            variant = cart_item.variations
            variant.stock += 1
            cart_item.delete()
            return JsonResponse({'removed': True})
    except:
        pass
    return redirect('cart')






def inc_cart(request, product_id, cart_item_id):
   
    # product = get_object_or_404(Product, id=product_id)

    product = Product.objects.get(id=product_id)
    print(product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(
                currentuser=request.user, id=cart_item_id)
            cart_items = CartItem.objects.filter(currentuser=request.user)
        else:            
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(cart=cart, id=cart_item_id)
            cart_items = CartItem.objects.filter(cart=cart)
            
        if cart_item.quantity > 0:
            variant = cart_item.variations            
            cart_item.quantity += 1
            cart_item.save()
            total = 0
            for cart_itm in cart_items:
                total += (cart_itm.variations.price * cart_itm.quantity)
            # tax = (2 * total)/100
            # grand_total = total + tax

            return JsonResponse({
                'price': cart_item.variations.price,
                'total': total,
                'quantity': cart_item.quantity,
                # 'cart_item': cart_item,
                # 'tax': tax,
                # 'grand_total': grand_total,
            })
        else:
          
              return JsonResponse({'message': 'Cannot increment . Quantity is already 0.'})

           
        
    except:
        pass
    return redirect('cart')
    # tax = 0
    # grand_total = 0
    

def remove_cart_item(request, product_id, cart_item_id):
    product = Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, product=product, currentuser=request.user, id=cart_item_id)
    else:
       cart = Cart.objects.get(cart_id=_cart_id(request))
       cart_item = get_object_or_404(CartItem, product=product, cart=cart, id=cart_item_id)
    
    cart_item.delete()
    return redirect('cart')


def checkout(request, total=0, quantity=0, cart_items=None):
    variants = SizeVariant.objects.filter()
    # request.session["redirect"] = request.build_absolute_uri()
    try:
        # tax = 0
        # grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(
                currentuser=request.user, is_active=True)
        else:
            
            # cart = Cart.objects.get(cart_id=_cart_id(request))
            # cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            return render(request, 'usertemplates/login.html')

        for cart_item in cart_items:
            total += (cart_item.variations.price * cart_item.quantity)
            quantity += cart_item.quantity
            if cart_item.quantity > cart_item.variations.stock:
                messages.info(
                    request, f'{cart_item.variations.product_id.product_name} is in out of stock')
                return redirect('cart')
        # tax = (2 * total)/100
        # grand_total = total + tax
    except ObjectDoesNotExist:
        pass  # just ignore
     # Get the current user and associated user profile
    current_user = request.user
    try:
     user_profile = Userprofile.objects.filter(currentuser=current_user)
    except Userprofile.DoesNotExist:
     user_profile = None

    addresses = None
    if user_profile:
     addresses = Userprofile.objects.filter(currentuser=current_user)

    default_address = None
    if user_profile:
     try:
        default_address = Userprofile.objects.get(currentuser=current_user, is_default=True)
     except Userprofile.DoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'address': user_profile,
        'addresses': addresses,  # Use 'addresses' instead of 'address'
        'user1': current_user,
        'ad': default_address,
    }

    
    return render(request, 'usertemplates/checkout.html',context)






def cart(request, total=0, quantity=0, cart_item=None):
    try:
        
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(
                currentuser=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart)

        for cart_item in cart_items:
            total += (cart_item.variations.price * cart_item.quantity)
            quantity += cart_item.quantity
        # tax = (2 * total)/100
        # grand_total = total + tax
        # applied_coupon = request.session.get('coupon_applied', None)
        # if applied_coupon:
        #     try:
        #         coupon = Coupon.objects.get(
        #             coupon_code=applied_coupon, is_expired=False, minimum_amount__lte=total)
        #         total -= coupon.discount_price
        #         grand_total = total + tax
        #     except Coupon.DoesNotExist:
        #         # Handle the case where the coupon does not exist or does not meet the minimum amount criteria
        #         pass
    except ObjectDoesNotExist:
        pass  # just ignore
    print(cart_items)
    context = {
        # 'applied_coupon': applied_coupon,
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        # 'tax': tax,
        # 'grand_total': grand_total,
    }
    
    return render(request, 'usertemplates/cart.html', context)

from django.shortcuts import HttpResponse, render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Prefetch
from .context_processors import get_cart_counter, get_cart_amount
from vendor.models import Vendor
from menu.models import Category, OnlineItem
from .models import Cart
from django.contrib.auth.decorators import login_required


# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count
    }

    return render(request, 'home/marketplace/listings.html', context)


def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)

    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'onlineitem',
            queryset = OnlineItem.objects.filter(is_available=True)
        )
    )
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items
    }
    return render(request, 'home/marketplace/vendor_detail.html', context)

  
def add_to_cart(request, item_id):
    if request.user.is_authenticated:
        if request.is_ajax():
            # check if the online item exits
            try:
                onlineitem = OnlineItem.objects.get(id=item_id)
                # check if user has already added that that item in the cart
                try:
                    checkcart = Cart.objects.get(user=request.user, onlineitem=onlineitem)
                    # increase the cart quantity
                    checkcart.quantity += 1
                    checkcart.save()
                    return JsonResponse({'status': 'success', 'message': 'increased the cart quanity', 'cart_counter': get_cart_counter(request), 'qty': checkcart.quantity, 'cart_amount': get_cart_amount(request)})
                except:
                    checkcart = Cart.objects.create(user=request.user, onlineitem=onlineitem, quantity=1)
                    return JsonResponse({'status': 'success', 'message': 'added the item to the cart', 'cart_counter': get_cart_counter(request), 'qty': checkcart.quantity,  'cart_amount': get_cart_amount(request)})
            except:
                return JsonResponse({'status': 'failed', 'message': 'This food does not exist'})
        else:
            return JsonResponse({'status': 'failed', 'message': 'Invalid request '})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})
    
def decrease_cart(request, item_id):
    if request.user.is_authenticated:
        if request.is_ajax():
            # check if the online item exits
            try:
                onlineitem = OnlineItem.objects.get(id=item_id)
                # check if user has already added that that item in the cart
                try:
                    checkcart = Cart.objects.get(user=request.user, onlineitem=onlineitem)
                    if checkcart.quantity > 1:
                        # decrease the cart quantity
                        checkcart.quantity -= 1
                        checkcart.save()
                    else:
                        checkcart.delete()
                        checkcart.quantity = 0
                    return JsonResponse({'status': 'success', 'message': 'Increased the cart quanity', 'cart_counter': get_cart_counter(request), 'qty': checkcart.quantity, 'cart_amount': get_cart_amount(request)})
                except:                       
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart',})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request '})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})

@login_required(login_url = 'login')  
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'home/marketplace/cart.html', context)
        
def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.is_ajax():
            try:
                # Check if the cart item exit
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_id:
                    cart_item.delete()
                    return JsonResponse({'status': 'Success', 'message': 'Cart item has been deleted!', 'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amount(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'Cart item does not exist'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
    


   
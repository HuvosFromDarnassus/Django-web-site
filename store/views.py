from django.views.generic import DetailView
from django.http import JsonResponse
from django.shortcuts import render
import datetime
import json

from .models import *
from .utils import *

"""
Views.

Describes the display on a web page.
"""

def store_view(request):
   """Returns context render for "Store" page.
   "Store" page view.
   """
   # Getting data from request.
   data = cartData(request)
   # Getting cartItems, order and items from request.
   cartItems = data['cartItems']
   order = data['order']
   items = data['items']
   # Getting all product objects from database.
   products = Product.objects.all()
   # Creating context.
   context = {
      'products': products,
      'cartItems': cartItems,
   }
   return render(request, 'store/store.html', context)

def cart_view(request):
   """Returns context render for "Cart" page.
   "Cart" page view.
   """
   # Getting data from request.
   data = cartData(request)
   # Getting cartItems, order and items from request.
   cartItems = data['cartItems']
   order = data['order']
   items = data['items']
   # Creating context.
   context = {
      'items': items,
      'order': order,
      'cartItems': cartItems,
   }
   return render(request, 'store/cart.html', context)

def checkout_view(request):
   """Returns context render for "Checkout" page.
   "Checkout" page view.
   """
   # Getting data from request.
   data = cartData(request)
   # Getting cartItems, order and items from request.
   cartItems = data['cartItems']
   order = data['order']
   items = data['items']
   # Creating context.
   context = {
      'items': items,
      'order': order,
      'cartItems': cartItems,
   }
   return render(request, 'store/checkout.html', context)

def update_item_view(request):
   """
   Gets productId and action from request,
   creates new orderItem and increment, decrement item quantity
   or deletes orderItem.
   """
   # Getting data from request json.
   data = json.loads(request.body)
   # Getting productId and action from request json.
   productId = data['productId']
   action = data['action']
   # Creating new customer based on user from request.
   customer = request.user.customer
   # Getting all product objects from database.
   product = Product.objects.get(id=productId)
   # Creating new order based on customer.
   order, created = Order.objects.get_or_create(customer=customer, complete=False)
   # Creating new orderItem based on order.
   orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
   # IF action is "add": increment orderItem quantity.
   if action == 'add':
      orderItem.quantity = (orderItem.quantity + 1)
   # IF action is "remove": decrement orderItem quantity.
   elif action == 'remove':
      orderItem.quantity = (orderItem.quantity - 1)
   # Save new orderItem in database.
   orderItem.save()
   # If orderItem quantity less or equals 0: delete orderItem from database.
   if orderItem.quantity <= 0:
      orderItem.delete()
   return JsonResponse('Item was added', safe=False)

def processOrder(request):
   """
   Creates and add new transaction id,
   creates new order and shipping for auth or guest user.
   """
   # Creating transaction id based on timestamp.
   transaction_id = datetime.datetime.now().timestamp()
   # Getting data from json request.
   data = json.loads(request.body)
   # If user is authenticated: Create new customer and new order.
   if request.user.is_authenticated:
      customer = request.user.customer
      order, created = Order.objects.get_or_create(customer=customer, complete=False)
   # If user is not logged in: Use guest user logic.
   else:
      customer, order = guestOrder(request, data)
   # Getting total price from json data.
   total = float(data['form']['total'])
   # Transaction id assignment.
   order.transaction_id = transaction_id
   # Total price security check, if equals: Create new order.
   if total == order.get_cart_total:
      order.complete = True
   order.save()
   # If there is at least one non-digital product: Create new ShippingAddress.
   if order.shipping == True:
         ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
         )
   return JsonResponse('Payment subbmitted...', safe=False)

def product_detail_view(request, id):
   """
   Gets product data from database by id,
   render data of one product in product detail page.
   """
   # Getting product object from database by id.
   obj = Product.objects.get(id=id)
   # Getting data from request for cart statement rendering.
   data = cartData(request)
   cartItems = data['cartItems']
   # Creating context.
   context = {
      'product': obj,
      'cartItems': cartItems,
   }
   return render(request, 'store/product_detail.html', context)
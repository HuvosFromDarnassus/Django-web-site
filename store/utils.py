import json
from .models import *

def cookieCart(request):
   """Returns data dic.

   Receives cookie json from request and prepares data from cookie to be sent to database.
   """
   # Except empty Cookie.
   try:
      cart = json.loads(request.COOKIES['cart'])
   except:
      cart = {}
   # Declare arrays and dics.
   items = []
   order = {
      'get_cart_total': 0,
      'get_cart_items': 0,
      'shipping': False,
   }
   cartItems = order['get_cart_items']
   # Cookie json parsing, putting data from json to arrays and to dics.
   for Id in cart:
      try:
         cartItems += cart[Id]['quantity']
         product = Product.objects.get(id=Id)
         total = (product.price * cart[Id]['quantity'])
         order['get_cart_total'] += total
         order['get_cart_items'] += cart[Id]['quantity']

         item = {
            'product':{
               'id': product.id,
               'name': product.name,
               'price': product.price,
               'imageURL': product.imageURL,
            },
            'quantity': cart[Id]['quantity'],
            'get_total': total,
         }
         items.append(item)
         # Digital product checking.
         if product.digital == False:
            order['shipping'] = True
      except:
         pass

   return {
      'cartItems': cartItems,
      'order': order,
      'items': items,
   }

def cartData(request):
   """Returns data dic.

   Creates new order for auth user and guest user.
   """
   # If user is authenticated: Create customer, order and get order items.
   if request.user.is_authenticated:
      customer = request.user.customer
      order, created = Order.objects.get_or_create(customer=customer, complete=False)
      items = order.orderitem_set.all()
      cartItems = order.get_cart_items
   # If user is not logged in: Get data from Cookie.
   else:
      cookieData = cookieCart(request)
      cartItems = cookieData['cartItems']
      order = cookieData['order']
      items = cookieData['items']

   return {
      'cartItems': cartItems,
      'order': order,
      'items': items,
   }

def guestOrder(request, data):
   """Returns guest customer and order.

   Creates order items and customer based on cookie data.
   """
   name = data['form']['name']
   email = data['form']['email']
   # Getting order items and customer from cookie data and creating new ones.
   cookieData = cookieCart(request)
   items = cookieData['items']
   customer, created = Customer.objects.get_or_create(email=email)
   customer.name = name
   customer.save()
   # Creating new order based on customer.
   order = Order.objects.create(
      customer=customer,
      complete=False
   )
   # Creating new orderItems.
   for item in items:
      product = Product.objects.get(id=item['product']['id'])
      orderItem = OrderItem.objects.create(
         product=product,
         order=order,
         quantity=(item['quantity'] if item['quantity']>0 else -1*item['quantity']),
      )
   return customer, order
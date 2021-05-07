from django.db import models
from django.contrib.auth.models import User

"""
Database Models.

Converts code to SQL and creates table in database.
"""

"""Customer model"""
class Customer(models.Model):
   user  = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
   name  = models.CharField(max_length=200, null=True)
   email = models.CharField(max_length=200)

   def __str__(self):
      return self.name

"""Product model"""
class Product(models.Model):
   name     = models.CharField(max_length=200)
   price    = models.FloatField()
   digital  = models.BooleanField(default=False, null=True, blank=True)
   image    = models.ImageField(null=True, blank=True)

   def __str__(self):
      return self.name

   @property
   def imageURL(self):
      """Returns image url on server."""
      try:
         url = self.image.url
      except:
         url = ''
      return url

"""Order model"""
class Order(models.Model):
   customer       = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
   date_ordered   = models.DateTimeField(auto_now_add=True)
   complete       = models.BooleanField(default=False)
   transaction_id = models.CharField(max_length=100, null=True)

   def __str__(self):
      return str(self.id)

   @property
   def shipping(self):
      """Returns False if there is at least one digital product."""
      shipping = False
      orderitems = self.orderitem_set.all()
      for item in orderitems:
         if item.product.digital == False:
            shipping = True
      return shipping

   @property
   def get_cart_total(self):
      """Returns total price for all products in order."""
      orderitems = self.orderitem_set.all()
      total = sum([item.get_total for item in orderitems])
      return total
   
   @property
   def get_cart_items(self):
      """Returns total quantity for all products in order."""
      orderitems = self.orderitem_set.all()
      total = sum([item.quantity  for item in orderitems])
      return total

"""OrderItem model"""
class OrderItem(models.Model):
   product     = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
   order       = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
   quantity    = models.IntegerField(default=0, null=True, blank=True)
   date_added  = models.DateTimeField(auto_now_add=True)

   @property
   def get_total(self):
      """Returns total price for one product type based on product price and quantity."""
      total = self.product.price * self.quantity
      return total

"""ShippingAddress model"""
class ShippingAddress(models.Model):
   customer    = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
   order       = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
   address     = models.CharField(max_length=200, null=False)
   city        = models.CharField(max_length=200, null=False)
   state       = models.CharField(max_length=200, null=False)
   zipcode     = models.CharField(max_length=200, null=False)
   date_added  = models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return self.address
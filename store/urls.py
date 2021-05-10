from django.urls import path

from .views import *

urlpatterns = [
   path('', store_view, name='store'),
   path('cart/', cart_view, name='cart'),
   path('checkout/', checkout_view, name='checkout'),
   path('update_item/', update_item_view, name='update_item'),
   path('process_order/', processOrder, name='process_order'),
   path('<int:id>', product_detail_view, name='product-detail')
]

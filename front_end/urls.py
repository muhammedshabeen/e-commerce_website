from django.urls import path
from .views import *

urlpatterns = [
   path('login',login,name="login"),
   path('',home,name="home"),
   path('about-us',about_us,name="about_us"),
   path('contact-us',contact_us,name="contact_us"),
   path('product',product,name="product"),
   path('product-detail/<slug:slug>',product_detail,name="product_detail"),
   path('add-to-cart',add_to_cart,name="add_to_cart"),
]
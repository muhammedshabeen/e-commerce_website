from django.urls import path
from .views import *

urlpatterns = [
   path('',home,name="home"),
   path('about-us',about_us,name="about_us"),
   path('contact-us',contact_us,name="contact_us"),
   path('product',product,name="product"),
   path('product-detail',product_detail,name="product_detail"),
]
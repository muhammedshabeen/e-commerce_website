from django.shortcuts import render, redirect
from django.http import HttpResponse
from master.models import *
from django.db.models import Prefetch
from django.contrib import messages


def home(request):
    product_objs = Product.objects.order_by('-id').prefetch_related(Prefetch('Product_Items', queryset=ProductVarients.objects.all()))[:10]
    print("product_objs",product_objs)
    context = {
        "product_objs":product_objs,
    }
    return render(request,'home/base.html',context)

def about_us(request):
    return render(request,'home/about_us.html')
def contact_us(request):
    return render(request,'home/contact_us.html')

def product(request):
    return render(request,'home/product.html')

def product_detail(request,slug):
    try:
        product_obj = Product.objects.prefetch_related(Prefetch('Product_Items', queryset=ProductVarients.objects.all())).get(slug=slug)
    except Product.DoesNotExist:
        messages.error(request,"Product not found")
        return redirect('home')
    context = {
        "product_obj":product_obj,
    }
    return render(request,'home/product_detail.html',context)

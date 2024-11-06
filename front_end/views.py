from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request,'home/base.html')

def about_us(request):
    return render(request,'home/about_us.html')
def contact_us(request):
    return render(request,'home/contact_us.html')

def product(request):
    return render(request,'home/product.html')

def product_detail(request):
    return render(request,'home/product_detail.html')

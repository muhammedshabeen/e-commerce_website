from django.shortcuts import render, redirect
from django.http import HttpResponse
from master.models import *
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login



def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request,email=email,password=password)
        if user is not None:
            # If the user is authenticated, log them in
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,"Invalid credentials")
            return redirect('login')
    return render(request,'registration/login.html')

@login_required
def logout(request):
    request.session.flush()
    return render(request,'registration/login.html')


def home(request):
    product_objs = Product.objects.order_by('-id')[:10]
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
        product_obj = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        messages.error(request,"Product not found")
        return redirect('home')
    context = {
        "product_obj":product_obj,
    }
    return render(request,'home/product_detail.html',context)

@login_required
def add_to_cart(request):
    with transaction.atomic():
        try:
            if request.method == 'POST':
                user = request.user
                print("User",user)
                product_id = request.POST.get('product_id')
                quantity = request.POST.get('quantity')
                size = request.data.get('size')
                CartTable.objects.create(user=user,product_id=product_id,quantity=quantity)
            else:
                print("Only Post method")
        except Exception as e:
            print("error",e)
    messages.error(request,"An error occurred")
    return redirect('home')
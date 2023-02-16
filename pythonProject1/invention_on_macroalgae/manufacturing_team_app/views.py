from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
import json
from .models import Manufacturing_team
from app1.models import *
from django.contrib import messages
from django.db.models.functions import Lower
from django.core.mail import send_mail
from datetime import datetime, timedelta

def home(request):
    return render(request,'index.html')

def mfta_signup(request):
    if request.method=="POST":
        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        phone = request.POST["phone"]
        address = request.POST["address"]

        Manufacturing_team(name=name,email=email,password=password,phone=phone,address=address).save()
        messages.success(request, 'Sucessfully Signed Up.')
    return render(request,'mf_ta/signup.html')

def mfta_login(request):
    if request.method=='POST':
        email=request.POST["email"]
        password=request.POST["password"]

        try:
            emp=Manufacturing_team.objects.get(email=email,password=password)
            messages.success(request, 'You Have Logged In')
            request.session['manuf'] = emp.email
            return redirect('/mfta_home/')

        except:
            return redirect('/mfta_login/')

    return render(request,'mf_ta/signup.html')

def mfta_logout(request):
    if 'manuf' in request.session:
        request.session.pop('manuf',None)
        messages.success(request,'Logout Successfully')
        return redirect('/')
    else:
        messages.success(request, 'Session Logged Out')
        return redirect('/mfta_signup/')

def mfta_home(request):
    return render(request,'mf_ta/home.html')

def count_time(request):
    try:
        sp = Specific_product.objects.filter(boolean=False)
        ps = Specific_product.objects.filter(boolean=False).values_list('product', flat=True)
        start_ = Specific_product.objects.filter(boolean=False).values_list('date_add', flat=True)
        dur = Specific_product.objects.filter(boolean=False).values_list('duration', flat=True)

        start_day = start_[0]
        dur_ = dur[0]

        products = Product.objects.get(name=ps[0])
        purchases = Purchase.objects.get(product=ps[0])

        # start_date = datetime.strptime(start_day, "%y-%m-%d")
        end_day = start_day + timedelta(days=30*dur_)


        stu={
            "pro_d":sp,'products': products,'purchases':purchases,'end_day':end_day
        }
        return render(request, 'mf_ta/product_status.html', stu)
    except:
        # messages.success(request, 'No products found in cart')
        return redirect('/count_time/')

def mail(request, id):
    x=Specific_product.objects.get(id=id)
    send_mail(
        'Product Status',
        'Product has been completed and ready for Shipping',
        'aakashbsurya@gmail.com',
        [x.email],
        fail_silently=False,
    )
    messages.info(request,"Sucessfuilly Sent Mail")
    return render(request,"mf_ta/admin_final.html/")

def approve_product(request):
    pd = Specific_product.objects.filter(boolean=False)
    return render(request, 'mf_ta/approve_product.html', {'pd': pd})

def admin_final(request):
    try:
        sp = Specific_product.objects.filter(boolean=False)
        ps = Specific_product.objects.filter(boolean=False).values_list('product', flat=True)
        start_ = Specific_product.objects.filter(boolean=False).values_list('date_add', flat=True)
        dur = Specific_product.objects.filter(boolean=False).values_list('duration', flat=True)

        start_day = start_[0]
        dur_ = dur[0]


        products = Product.objects.get(name=ps[0])
        purchases = Purchase.objects.get(product=ps[0])

        # start_date = datetime.strptime(start_day, "%y-%m-%d")
        end_day = start_day + timedelta(days=30*dur_)



        stu={
            "pro_d":sp,'products': products,'purchases':purchases,'end_day':end_day
        }
        return render(request,'mf_ta/admin_final.html',stu)
    except:
        # messages.success(request, 'No products found in cart')
        return render(request,'mf_ta/mfta_home/')

def progress_bar(request):
    try:
        return render(request, 'mf_ta/progress_bar.html')
    except:
        print("ok")
    return redirect('/count_time/')

from django.shortcuts import render,redirect
from django.http import HttpResponse
from app1.models import *
from django.contrib import messages
from datetime import datetime, timedelta

def home(request):
    return render(request,'index.html')

def admin_home(request):
    return render(request,'admin/home.html')

def admin_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if email == "admin@gmail.com" and password == "admin":
            request.session['admin'] = 'admin@gmail.com'
            messages.info(request, "Successfully Login")
            return redirect('/admin_home/')
        elif email != "admin@gmail.com":
            messages.error(request, "Wrong Admin Email")
            return redirect('/admin_login/')
        elif password != "admin":
            messages.error(request, "Wrong Admin Password")
            return redirect('/admin_login/')
    return render(request, 'admin/signup.html')

def about(request):
    return render(request,'admin/signup.html')

def admin_logout(request):
    if 'admin' in request.session:
        request.session.pop('admin',None)
        messages.success(request,'Logout Successfully')
        return redirect('/')
    else:
        messages.success(request, 'Session Logged Out')
        return redirect('/admin_logout/')

def access_domain_team(request):
    datas=Product_looking_for.objects.all()
    return render(request, 'admin/company_details.html',{'datas':datas})

def prediction_detail(request):
    da=Specific_product.objects.filter(boolean=False)
    return render(request,'admin/prediction_details.html',{'da':da})

def process_details(request):
    pd = Specific_product.objects.filter(boolean=False)
    return render(request, 'admin/process_details.html', {'pd': pd})

def send_process_team(request,id):
    datas = Specific_product.objects.get(id=id)
    datas.boolean=True
    datas.save()
    print('hi')
    messages.info(request, "INFORMATION FORWARDED PROCESS TEAM")
    return redirect('/admin_home/')

def s_manufacturing_team(request):
    pd = Specific_product.objects.filter(boolean=False)
    return render(request, 'admin/process_details.html',{'pd':pd})

def send_manufacturing_team(request,id):
    ans=Specific_product.objects.get(id=id)
    ans.boolean=False
    ans.save()
    messages.info(request, "APPROVED...PROCEED FURTHER TO MANUFACTURING TEAM")
    return redirect('/admin_home/')

def pay_slip(request):
    sp = Specific_product.objects.filter(boolean=False)
    ps = Specific_product.objects.filter(boolean=False).values_list('product', flat=True)
    c_name = Product_looking_for.objects.values_list('company_name', flat=True)
    dur = Product_looking_for.objects.values_list('email', flat=True)
    duration = Specific_product.objects.filter(boolean=False).values_list('duration', flat=True)

    start_ = Specific_product.objects.filter(boolean=False).values_list('date_add', flat=True)

    p = Product_looking_for.objects.get(company_name=c_name[0])
    products = Product.objects.get(name=ps[0])
    purchases = Purchase.objects.get(product=ps[0])

    start_day = start_[0]
    dur_ = duration[0]
    print(start_day)
    print(dur_)
    end_day = start_day + timedelta(days=30 * dur_)

    c = c_name[0]
    d_ = dur[0]
    f=purchases.total

    final = [f+50+49]
    f=final[0]

    stu = {
        "pro_d": sp, 'products': products, 'purchases': purchases, 'c':c,'d_':d_,'c_name':c_name,'p':p,'f':f,'end_day':end_day,
    }
    if request.method == "POST":
        company_name = request.POST["company_name"]
        email = request.POST["email"]
        product = request.POST["product"]
        amount = request.POST["amount"]
        try:
            Pay_slips(company_name=company_name, email=email, product=product, amount=amount).save()
            messages.success(request, 'Sucessfully  Added To User.')
            return redirect('/admin_home/')
        except:
            print("Hello")

    return render(request,'admin/pay_slip.html',stu)

def notify_user(request):
    messages.success(request, 'Notified To User.')
    return redirect('/admin_home/')

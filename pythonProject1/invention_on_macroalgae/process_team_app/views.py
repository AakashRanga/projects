from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Process_team
from app1.models import *
from django.contrib import messages
from django.core.mail import send_mail
from django.template import loader
import numpy as np
import pandas as pd
from sklearn.linear_model import RidgeClassifier
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
import warnings

warnings.filterwarnings('ignore')

def home(request):
    return render(request,'index.html')

def process_signup(request):
    if request.method=="POST":
        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        phone = request.POST["phone"]
        address = request.POST["address"]

        Process_team(name=name,email=email,password=password,phone=phone,address=address).save()
        messages.success(request, 'Sucessfully Signed Up.')
    return render(request,'process_team/signup.html')

def process_login(request):
    if request.method=='POST':
        email=request.POST["email"]
        password=request.POST["password"]

        try:
            emp=Process_team.objects.get(email=email,password=password)
            messages.success(request, 'You Have Logged In')
            request.session['process'] = emp.email
            return redirect('/process_home/')

        except:
            return redirect('/process_login/')

    return render(request,'process_team/signup.html')

def process_logout(request):
    if 'process' in request.session:
        request.session.pop('process',None)
        messages.success(request,'Logout Successfully')
        return redirect('/')
    else:
        messages.success(request, 'Session Logged Out')
        return redirect('/process_signup/')

def process_home(request):
    return render(request,'process_team/home.html')

def algo(datas,r):
    data = pd.read_csv("Dataset/akash1.csv")
    data_x = data.iloc[:, :-1]
    data_y = data.iloc[:, -1]
    string_datas = [i for i in data_x.columns if data_x.dtypes[i] == np.object_]

    LabelEncoders = []
    for i in string_datas:
        newLabelEncoder = LabelEncoder()
        data_x[i] = newLabelEncoder.fit_transform(data_x[i])
        LabelEncoders.append(newLabelEncoder)
    ylabel_encoder = None
    if type(data_y.iloc[1]) == str:
        ylabel_encoder = LabelEncoder()
        data_y = ylabel_encoder.fit_transform(data_y)

    model = RidgeClassifier()
    model.fit(data_x, data_y)

    value = {data_x.columns[i]: datas[i] for i in range(len(datas))}
    l = 0
    for i in string_datas:
        z = LabelEncoders[l]
        value[i] = z.transform([value[i]])[0]
        l += 1
    value = [i for i in value.values()]
    predicted = model.predict([value])
    print(12334455)
    if ylabel_encoder:
        predicted = ylabel_encoder.inverse_transform(predicted)
    return predicted[0]

def get_input(request, id):
    # if 'user' in request.session:
    get = Specific_product.objects.get(id=id)
    r=get.id
    inputvar = []
    get.save()
    product= get.product
    reason= get.reason
    quantity= get.quantity
    duration=get.duration
    quality= get.quality

    inputvar.append(product)
    inputvar.append(reason)
    inputvar.append(quantity)
    inputvar.append(duration)
    inputvar.append(quality)

    print('input:', inputvar)
    ka = algo(inputvar,r)
    print('OUTPUT:',ka)
    st = Specific_product.objects.filter(id=r).update(solution=ka)
    messages.success(request, 'Sucessfully Predicted.')
    return redirect('/view_predction/')

def prediction_(request):
    ds = Specific_product.objects.filter(boolean=True)
    return render(request,'process_team/prediction.html',{'ds':ds})

def view_predction(request):
    ds = Specific_product.objects.filter(boolean=True)
    return render(request,'process_team/view_predection.html',{'ds':ds})

def send_view_predction(request):
    ds = Specific_product.objects.filter(boolean=False)
    return render(request,'process_team/view_predection.html',{'ds':ds})

def send_admin_team(request,id):
    datas = Specific_product.objects.get(id=id)
    datas.boolean=False
    datas.save()
    print('hi')
    messages.info(request, "INFORMATION FORWARDED TO ADMIN TEAM")
    return redirect('/view_predction/')

def snd_manufacturing_team(request):
    final = Specific_product.objects.filter(boolean=True)
    return render(request, 'process_team/manu.html', {'final': final})

def get_manufacturing(request):
    final=Specific_product.objects.filter(boolean=False)
    return render(request,'process_team/manu.html',{'final':final})

def get_manufacturing_team(request,id):
    re = Specific_product.objects.get(id=id)
    re.boolean = False
    re.save()
    print('hi')
    messages.info(request, "INFORMATION FORWARDED MANUFACTURING TEAM")
    return redirect('/snd_manufacturing_team/')





from django.shortcuts import render,redirect
from .models import Details
from django.contrib import messages
from django.core.mail import send_mail
# Create your views here.
def signup(request):
    if request.method=="POST":
        name=request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        number = request.POST["number"]
        address = request.POST["address"]
        image = request.FILES["image"]
        file = request.FILES["file"]
        Details(name=name,email=email,password=password,number=number,address=address,image=image,file=file).save()
        messages.success(request, 'Sucessfully signed up.')
    return render(request,'index.html')

def login(request):
    if request.method=='POST':
        email=request.POST["email"]
        password=request.POST["password"]
        print(email)
        print(password)
        try:
            t=Details.objects.get(email=email,password=password)
            print(email)
            print(password)
            messages.success(request, 'You have logged in')
            return redirect('/home/')

        except:
            print(email)
            print(password)
            return redirect('/login/')
        print("done")
    return render(request,'login.html')

def home(request):
    data=Details.objects.all()
    return render(request,'home.html',{'data':data})

def update(request, id):
    x= Details.objects.get(id=id)

    if request.method == 'POST':
        x.name = request.POST['name']
        x.email = request.POST['email']
        x.number = request.POST['number']
        x.address = request.POST['address']
        x.save()
        try:
            x.save()
            messages.success(request, 'Profile details updated.')
            return redirect('/home/')
        except:
            return redirect('/update/<int:id>/')
        # messages.warning(request, 'Are you sure you want edit details')
    return render(request, 'update.html', {'x':x})

    # template = loader.get_template(update.html)
    # context={
    #     'mymember' : mymember,
    # }

def delete(request, id):
    y=Details.objects.get(id=id)
    y.delete()
    messages.warning(request, 'You have deleted a user')
    return redirect('/home/')

def mail(request, id):
    x=Details.objects.get(id=id)
    send_mail(
        'Subject here',
        'Hello There',
        'aakashbsurya@gmail.com',
        [x.email],
        fail_silently=False,
    )
    messages.info(request,"sucessfuilly send mail")
    return redirect("/home/")
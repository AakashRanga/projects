from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
import json
from datetime import datetime, timedelta
from .models import *
from django.contrib import messages
from django.core.mail import send_mail
from .utils import cookieCart, cartData, guestOrder


def home(request):
    return render(request,'index.html')

def contacts(request):
    return render(request,'contact.html')

def signup(request):
    if request.method=="POST":
        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        company_name = request.POST["company_name"]
        phone = request.POST["phone"]
        address = request.POST["address"]

        Client(name=name,email=email,password=password,company_name=company_name,phone=phone,address=address).save()
        messages.success(request, 'Sucessfully Signed Up.')
    return render(request,'client/signup.html')

def purchase(request):
    if request.method=="POST":
        name = request.POST["name"]
        email = request.POST["email"]
        address = request.POST["address"]
        city = request.POST["city"]
        state = request.POST["state"]
        zipcode = request.POST["zipcode"]
        country = request.POST["country"]
        # image = request.FILES["image"]
        product = request.POST["product"]
        price = request.POST["price"]
        quantity = request.POST["quantity"]
        items = request.POST["items"]
        total = request.POST["total"]
        Purchase(name=name,email=email,address=address,city=city,state=state,zipcode=zipcode,country=country,product=product,price=price,quantity=quantity,items=items,total=total).save()
        messages.success(request, 'Product Has Been Added')
    return render(request, 'store/checkout.html')


def product_looking_for(request):
    if request.method == "POST":
        company_name = request.POST["company_name"]
        phone_number = request.POST["phone_number"]
        email = request.POST["email"]
        company_type = request.POST["company_type"]
        product = request.POST["product"]
        licence_number = request.POST["licence_number"]
        licence_document = request.POST["licence_document"]
        address = request.POST["address"]
        city = request.POST["city"]
        state = request.POST["state"]
        pin = request.POST["pin"]
        country = request.POST["country"]
        message = request.POST["message"]
        Product_looking_for(company_name=company_name,phone_number=phone_number,email=email,company_type=company_type,product=product,licence_number=licence_number,licence_document=licence_document,address=address,city=city,state=state,pin=pin,country=country,message=message).save()
        messages.success(request, 'Details Has Been Saved.')
    return render(request, 'client/product_looking_for.html')

def product_specification(request):
    if request.method == "POST":
        product = request.POST["product"]
        reason = request.POST["reason"]
        quantity = request.POST["quantity"]
        duration = request.POST["duration"]
        quality = request.POST["quality"]
        email = request.POST["email"]
        Specific_product(product=product,reason=reason,quantity=quantity,duration=duration,quality=quality,email=email).save()
        messages.success(request, 'Your Request Has Been Noted')
    return render(request, 'client/specific_product.html')

def login(request):
    if request.method=='POST':
        email=request.POST["email"]
        password=request.POST["password"]

        try:
            emp=Client.objects.get(email=email,password=password)
            messages.success(request, 'You Have Logged In')
            request.session['client'] = emp.email
            return render(request,'client/home.html')

        except:
            return redirect('/login/')

    return render(request,'client/signup.html')

def client_logout(request):
    if 'client' in request.session:
        request.session.pop('client',None)
        messages.success(request,'Logout Successfully')
        return redirect('/')
    else:
        messages.success(request, 'Session Logged Out')
        return redirect('/signup/')

def client_home(request):
    return render(request,'client/home.html')

def newproduct(request):
    return render(request,'client/product_new.html')

def contact(request):
    return render(request,'client/client_contact.html')

def about(request):
    return render(request,'about.html')

def purchased(request):
    d = Purchase.objects.all()
    return render(request, 'client/purchased.html', {'d': d})


def store(request):

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

# from django.views.decorators.csrf import csrf_exempt
#
# @csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)

def manu_team(request):
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
        return render(request, 'admin/manu_team.html', stu)
    except:
        # messages.success(request, 'No products found in cart')
        return redirect('/manu_t/')

def c_mail(request, id):
    x=Specific_product.objects.get(id=id)
    send_mail(
        'Payment Completed',
        'The payment of client has been sucessfully completed and you may start the shipping now',
        'aakashbsurya@gmail.com',
        [x.email],
        fail_silently=False,
    )

    messages.info(request, "Payment Has Been Sucessfully Completed")
    return redirect('/client_home/')

def payment(request):
    sp = Specific_product.objects.filter(boolean=False)
    ps = Specific_product.objects.filter(boolean=False).values_list('product', flat=True)
    g = Specific_product.objects.filter(boolean=False).values_list('email', flat=True)

    products = Product.objects.get(name=ps[0])
    purchases = Purchase.objects.get(product=ps[0])
    g_d = g[0]

    f = purchases.total

    final = [f + 50 + 49]

    stu = {
        "pro_d": sp, 'products': products, 'purchases': purchases, 'g_d':g_d,'final':final[0]
    }

    return render(request, 'client/payment.html',stu)
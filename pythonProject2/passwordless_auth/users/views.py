from django.core.mail import send_mail
from django.shortcuts import render,redirect
from .models import *
from hacker.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from django.shortcuts import render
import openai
# Create your views here.



def home(request):
    return render(request,'home/index.html')

def se(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        se_details(username=username,password=password).save()
        messages.success(request, 'SUCCESSFULLY UPDATED.')
        return redirect('/admin_home/')
    return render(request,'hacker/index.html')

def about(request):
    return render(request,'home/about.html')

def frontpage(request):
    return render(request, 'core/frontpage.html')

def m_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/frontpage/')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})

def signup(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        phone = request.POST["phone"]
        f1 = request.POST["f1"]
        f2 = request.POST["f2"]
        f3 = request.POST["f3"]
        f4 = request.POST["f4"]
        f5 = request.POST["f5"]

        users_details(name=name,email=email,password=password,phone=phone,f1=f1,f2=f2,f3=f3,f4=f4,f5=f5).save()
        messages.success(request, 'Sucessfully Signed Up.')

    return render(request,'login/user_login.html')

# def user_logout(request):
#     if 'user' in request.session:
#         request.session.pop('user',None)
#         messages.success(request,'Logout Successfully')
#         return redirect('/')
#     else:
#         email = request.session.get('email')
#         user = users_details.objects.get(email=email)
#         user_app = user_approve.objects.get(email=email)
#         user_app.delete()
#         print("content",email)
#         print("status:",user.admin_status)
#         print("status:", user.approved)
#         user.admin_status = 0
#         user.save()
#         user.approved = 0
#         user.save()
#         print("status:", user.approved)
#         print("status:", user.admin_status)
#         messages.success(request, 'Session Logged Out')
#         request.session.pop('email', None)
#         return redirect('/login_page/')

def user_logout(request):
    if 'user' in request.session:
        request.session.pop('user', None)
        messages.success(request, 'Logout Successfully')
        return redirect('/')
    else:
        email = request.session.get('email')
        user = users_details.objects.get(email=email)
        user_apps = user_approve.objects.filter(email=email)
        user_apps.delete()
        user.admin_status = 0
        user.save()
        user.approved = 0
        user.save()
        messages.success(request, 'Session Logged Out')
        request.session.pop('email', None)
        return redirect('/login_page/')

def admin_home(request):
    email = request.session.get('email')
    if email:
        user = users_details.objects.get(email=email)
        try:
            u_ = user_approve.objects.latest('id').id
            u = user_approve.objects.get(id=u_)
            return render(request, 'admin/admin_home.html',{'u':u,'user':user})
        except user_approve.DoesNotExist:
            return render(request, 'admin/admin_home.html',{'user':user})
    else:
        return redirect('/login_page/')

def allow_users(request):
    email = request.session.get('email')
    user = users_details.objects.get(email=email)
    d = user_approve.objects.all()
    return render(request,'admin/allow_users.html',{'user':user,'d':d})

def approve(request,id):
    user_app = user_approve.objects.get(id=id)
    user = users_details.objects.get(email=user_app.email)
    d = user_approve.objects.all()
    user_app.approved = 1
    user_app.status ="Approved"
    user_app.save()
    user.approved = 1
    user.save()
    return render(request,'admin/allow_users.html',{'user_app':user_app,'d':d})

def reject(request,id):
    user_app = user_approve.objects.get(id=id)
    d = user_approve.objects.all()
    user_app.approved = 0
    user_app.status = "Reject"
    user_app.save()
    return render(request, 'admin/allow_users.html', {'user_app': user_app, 'd': d})

def delete_users(request,id):
    user_app = user_approve.objects.get(id=id)
    d=user_approve.objects.all()
    user_app.delete()
    return render(request,'admin/allow_users.html',{'user_app':user_app, 'd':d})

def user_login(request):
    if request.method=='POST':
        email=request.POST["email"]
        password=request.POST["password"]

        try:
            emp=users_details.objects.get(email=email,password=password)
            messages.success(request, 'You Have Logged In')
            request.session['user'] = emp.email
            return redirect('/admin_home/')
        except:
            messages.success(request,"Unauthorized user name and password")
            return redirect('/login_page/')
    return render(request,'login/user_login.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = users_details.objects.get(email=email)
            pattern = [user.f1, user.f2, user.f3, user.f4]
            q_pattern = [user.a1, user.a2, user.a3, user.a4]
            lpattern = [user.f1, user.f2, user.f3, user.f4, user.f5]
            lq_pattern = [user.a1, user.a2, user.a3, user.a4, user.a5]
            emp = users_details.objects.get(email=email, password=password)
            user = users_details.objects.get(email=email)
            request.session['email'] = user.email

            if (user.login_attempts== 0):

                x = user_approve.objects.create(
                    name=users_details.objects.filter(email=user.email).values_list('name', flat=True)[0],
                    email=users_details.objects.filter(email=user.email).values_list('email', flat=True)[0],
                    password=users_details.objects.filter(email=user.email).values_list('password', flat=True)[0],
                )

                u_ = user_approve.objects.latest('id').id
                print(u_)
                u = user_approve.objects.get(id=u_)
                print(u)
                user.pattern = "s"

                # null_records = user_approve.objects.filter(Q(name__isnull=True)).values_list('id', flat=True)
                # null_record_ids = list(null_records)
                # print('vimal:',null_record_ids)

                user.save()
                messages.success(request, 'You Have Logged In')
                return render(request, 'admin/admin_home.html',{'u':u})

            elif (user.login_attempts==1):
                user.a2 = "s"
                user.save()
                user.login_attempts += 1
                user.save()
                pat = users_details.objects.get(email=email)
                pat.pattern = "s"
                messages.success(request, 'You Have Logged In')
                pat.save()

            elif (user.login_attempts==2):
                user.a3 = "s"
                user.save()
                user.login_attempts += 1
                user.save()
                pat = users_details.objects.get(email=email)
                pat.pattern = "s"
                messages.success(request, 'You Have Logged In')
                pat.save()

            elif (user.login_attempts==3):
                user.a4 = "s"
                user.save()
                user.login_attempts += 1
                user.save()
                pat = users_details.objects.get(email=email)
                pat.pattern = "s"
                messages.success(request, 'You Have Logged In')
                pat.save()

            elif user.login_attempts==4:

                user.a5 = "s"
                user.save()
                user.login_attempts += 1
                user.save()
                pat = users_details.objects.get(email=email)
                pat.pattern = "s"
                messages.success(request, 'You Have Logged In')
                pat.save()

            elif user.login_attempts==5:
                if lpattern==lq_pattern:
                    user.approved = 1
                    user.save()
                    user.admin_status = 1
                    user.save()
                    user = users_details.objects.get(email=email)
                    user.login_attempts = 0
                    user.save()
                    user.a1=0
                    user.save()
                    user.a2=0
                    user.save()
                    user.a3=0
                    user.save()
                    user.a4=0
                    user.save()
                    user.a5=0
                    user.save()

                    messages.success(request, 'You Have Logged In')
                    return render(request, 'admin/admin_home.html', {'user': user})
                else:
                    user.login_attempts = 0
                    user.save()
                    messages.success(request, 'Too Many Access Try Later')
                    return redirect('/')

        except:

            user = users_details.objects.get(email=email)
            lpattern = [user.f1, user.f2, user.f3, user.f4, user.f5]
            lq_pattern = [user.a1, user.a2, user.a3, user.a4, user.a5]

            if (user.login_attempts==0):
                # increment login attempts
                user.a1="f"
                user.save()
                user.login_attempts += 1
                user.save()
                pat = users_details.objects.get(email=email)
                user.pattern = "f"
                messages.success(request, "Unauthorized user name and password")
                user.save()

            elif (user.login_attempts==1):
                user.a2 = "f"
                user.save()
                user.login_attempts += 1
                user.save()
                pat = users_details.objects.get(email=email)
                pat.pattern = "f"
                messages.success(request, "Unauthorized user name and password")
                pat.save()

            elif (user.login_attempts==2):
                user.a3 = "f"
                user.save()
                user.login_attempts += 1
                user.save()
                pat = users_details.objects.get(email=email)
                pat.pattern = "f"
                messages.success(request, "Unauthorized user name and password")
                pat.save()

            elif (user.login_attempts==3):
                user.a4 = "f"
                user.save()
                user.login_attempts += 1
                user.save()
                pat = users_details.objects.get(email=email)
                pat.pattern = "f"
                messages.success(request, "Unauthorized user name and password")
                pat.save()

            elif user.login_attempts==4 :
                user.a5 = "f"
                user.save()
                user.login_attempts += 1
                user.save()
                pat = users_details.objects.get(email=email)
                pat.pattern = "f"
                messages.success(request, "Unauthorized user name and password",{'user':user})
                pat.save()

            elif user.login_attempts==5:
                if lpattern==lq_pattern:
                    user.approved = 1
                    user.save()
                    user.admin_status = 1
                    user.save()
                    user = users_details.objects.get(email=email)
                    user.login_attempts = 0
                    user.save()
                    user.a1=0
                    user.save()
                    user.a2=0
                    user.save()
                    user.a3=0
                    user.save()
                    user.a4=0
                    user.save()
                    user.a5=0
                    user.save()

                    messages.success(request, 'You Have Logged In')
                    return render(request, 'admin/admin_home.html', {'user': user})

                else:
                    user.login_attempts = 0
                    user.save()
                    messages.success(request, 'Too Many Access Try Later')
                    return redirect('/')
    return render(request, 'login/user_login.html')

def robot_home(request):
    return render(request, 'robot/index.html')

def un_users(request):
    users = user_approve.objects.all()
    return render(request,'robot/un_users.html',{"users":users})

def ano_users(request):
    null_records = user_approve.objects.filter(name__isnull=True)
    context = {'null_records': null_records}
    return render(request, 'robot/ano_users.html', context)
# def mail(request, id):
#     x=Specific_product.objects.get(id=id)
#     send_mail(
#         'Product Status',
#         'Product has been completed and ready for Shipping',
#         'aakashbsurya@gmail.com',
#         [x.email],
#         fail_silently=False,
#     )
#     messages.info(request,"Sucessfuilly Sent Mail")
#     return render(request,"mf_ta/admin_final.html/")
def intimate_to_sec(request,id):
    user_app = user_approve.objects.get(id=id)
    email=user_app.email
    print(email)
    send_mail(
        'Security Alert',
        'There has been an attempt to break your accounts security, but dont worry—well take care of it in accordance '
        'with our security protocol. Please adhere to the safety precautions. Keep smiling, And stay safe.',
        'aakashbsurya@gmail.com',
        [user_app.email],
        fail_silently=False,
    )
    user = users_details.objects.get(email=email)
    user.secure= False
    user.save()
    user_app.approved = 0
    user_app.boolean = True
    user_app.save()
    messages.info(request, "INFORMATION FORWARDED TO SECURITY TEAM")
    return render(request, 'robot/ano_users.html', {'user_app': user_app})

def release(request):
    inactive_users = users_details.objects.filter(secure=False)
    return render(request,'robot/release.html',{'inactive_users':inactive_users})

def fall_in(request,id):
    user = users_details.objects.get(id=id)
    user.secure = True
    user.save()
    return render(request,'robot/release.html',{'user':user})

def delete_INTRUDERS(request,id):
    user_app = user_approve.objects.get(id=id)
    x = invaded_acc.objects.create(
        email=users_details.objects.filter(email=user_app.email).values_list('email', flat=True)[0],
        password=users_details.objects.filter(email=user_app.email).values_list('password', flat=True)[0],
    )
    print('x:', x.email)
    user_app.delete()
    return render(request,'security/ex_intru.html',{'user_app':user_app})

def security_home(request):
    return render(request,'security/home.html')
def security_ex_intru(request):
    pd = user_approve.objects.filter(boolean=True)
    return render(request,'security/ex_intru.html',{'pd':pd})
def security_in_acc(request):
    u = invaded_acc.objects.all()
    return render(request,'security/in_acc.html',{'u':u})
def in_push(request, id):
    x= invaded_acc.objects.get(id=id)
    return render(request, 'security/sec_acc.html',{'x': x})
def security_sec_acc(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = users_details.objects.filter(email=email).first()
        if user:
            user.email = email
            user.password = password
            user.save()
            u = invaded_acc.objects.get(email=email)
            u.delete()
            messages.success(request, 'Password Reset Has Done Successfully')
        else:
            messages.error(request, 'User with this email does not exist')
    return render(request, 'security/sec_acc.html')
def security_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = users_details.objects.get(email=email)
            pattern = [user.f1, user.f2, user.f3, user.f4]
            q_pattern = [user.a1, user.a2, user.a3, user.a4]
            lpattern = [user.f1, user.f2, user.f3, user.f4, user.f5]
            lq_pattern = [user.a1, user.a2, user.a3, user.a4, user.a5]
            emp = users_details.objects.get(email=email, password=password)
            user = users_details.objects.get(email=email)
            request.session['email'] = user.email

            if (user.login_attempts==1):
                user.a2 = "s"
                user.save()
                user.login_attempts += 1
                user.save()
                pat = users_details.objects.get(email=email)
                pat.pattern = "s"
                messages.success(request, 'You Have Logged In')
                pat.save()

            elif (user.login_attempts==2):
                user.a3 = "s"
                user.save()
                user.login_attempts += 1
                user.save()
                pat = users_details.objects.get(email=email)
                pat.pattern = "s"
                pat.save()

            elif (user.login_attempts==3):
                user.a4 = "s"
                user.save()
                user.login_attempts += 1
                user.save()
                pat = users_details.objects.get(email=email)
                pat.pattern = "s"
                messages.success(request, 'You Have Logged In')
                pat.save()

            elif user.login_attempts==4:
                if pattern == q_pattern:
                    user.approved = 1
                    user.save()
                    user.a5 = "s"
                    user.save()
                    user.login_attempts += 1
                    user.save()
                    pat = users_details.objects.get(email=email)
                    pat.pattern = "s"
                    messages.success(request, 'You Have Logged In')
                    pat.save()

            elif user.login_attempts==5:
                if lpattern==lq_pattern:
                    user.admin_status = 1
                    user.save()
                    user = users_details.objects.get(email=email)
                    user.login_attempts = 0
                    user.save()
                    user.a1=0
                    user.save()
                    user.a2=0
                    user.save()
                    user.a3=0
                    user.save()
                    user.a4=0
                    user.save()
                    user.a5=0
                    user.save()
                    messages.success(request, 'You Have Logged In')
                    return render(request, 'security/home.html', {'user': user})
                else:
                    user.login_attempts = 0
                    user.save()
                    messages.success(request, 'Too Many Access Try Later')
                    return redirect('/')

        except:

            user = users_details.objects.get(email=email)
            lpattern = [user.f1, user.f2, user.f3, user.f4, user.f5]
            lq_pattern = [user.a1, user.a2, user.a3, user.a4, user.a5]

            if (user.login_attempts==0):
                # increment login attempts
                user.a1="f"
                user.save()
                user.login_attempts += 1
                user.save()
                pat = users_details.objects.get(email=email)
                user.pattern = "f"
                messages.success(request, "Unauthorized user name and password")
                user.save()

            elif (user.login_attempts==1):
                user.a2 = "f"
                user.save()
                user.login_attempts += 1
                user.save()
                pat = users_details.objects.get(email=email)
                pat.pattern = "f"
                messages.success(request, "Unauthorized user name and password")
                pat.save()

            elif (user.login_attempts==2):
                user.a3 = "f"
                user.save()
                user.login_attempts += 1
                user.save()
                pat = users_details.objects.get(email=email)
                pat.pattern = "f"
                messages.success(request, "Unauthorized user name and password")
                pat.save()

            elif (user.login_attempts==3):
                user.a4 = "f"
                user.save()
                user.login_attempts += 1
                user.save()
                pat = users_details.objects.get(email=email)
                pat.pattern = "f"
                messages.success(request, "Unauthorized user name and password")
                pat.save()

            elif user.login_attempts==4 :
                user.a5 = "f"
                user.save()
                user.login_attempts += 1
                user.save()
                pat = users_details.objects.get(email=email)
                pat.pattern = "f"
                messages.success(request, "Unauthorized user name and password",{'user':user})
                pat.save()

            elif user.login_attempts==5:
                if lpattern==lq_pattern:

                    user.admin_status = 1
                    user.save()
                    user = users_details.objects.get(email=email)
                    user.login_attempts = 0
                    user.save()
                    user.a1=0
                    user.save()
                    user.a2=0
                    user.save()
                    user.a3=0
                    user.save()
                    user.a4=0
                    user.save()
                    user.a5=0
                    user.save()

                    messages.success(request, 'You Have Logged In')
                    return render(request, 'security/home.html', {'user': user})

                else:
                    user.login_attempts = 0
                    user.save()
                    messages.success(request, 'Too Many Access Try Later')
                    return redirect('/')

    return render(request,'security/login.html')


openai.api_key = "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"

def chatbot_response(request):
    email = request.session.get('email')
    user = users_details.objects.get(email=email)
    try:
        if request.method == 'POST':
            prompt = request.POST.get('prompt')
            model_engine = "text-davinci-003"
            completion = openai.Completion.create(
                engine=model_engine,
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            )
            response = completion.choices[0].text
            return render(request, 'bot/chatbot_response.html', {'response': response})
    except:
        messages.success(request, 'Im Here to give you Useful Content' )
    return render(request, 'bot/chatbot.html',{'user':user})


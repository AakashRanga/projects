from django.contrib.auth import authenticate
from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from users.models import *
from django.db.models import Q

def attacker_home(request):
    return render(request,'hacker/home.html')

def user_details(request):
    datas=se_details.objects.all()
    return render(request,'hacker/user_details.html',{'datas':datas})

def hacked_details(request,id):
    datas= se_details.objects.get(id=id)
    # return render(request, 'hacker/user_details.html', {'datas': datas})
    return redirect('/ha_login/<int:id>/')

def update(request, id):
    x= se_details.objects.get(id=id)
    return render(request, 'hacker/hacker_login.html',{'x': x})

def hacker_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        user_detail = users_details.objects.filter(email=email).values_list('f1', 'f2', 'f3', 'f4', 'f5')
        x = list(user_detail)
        user = users_details.objects.get(email=email)
        pattern = [user.f1, user.f2, user.f3, user.f4]
        q_pattern = [user.a1, user.a2, user.a3, user.a4]
        lpattern = [user.f1, user.f2, user.f3, user.f4, user.f5]
        lq_pattern = [user.a1, user.a2, user.a3, user.a4, user.a5]
        print(pattern)
        print(q_pattern)
        print(user.approved)

        try:
            emp = users_details.objects.get(email=email, password=password)
            user = users_details.objects.get(email=email)
            request.session['email'] = user.email
            if (user.login_attempts == 0):

                x = user_approve.objects.create(
                    email=users_details.objects.filter(email=user.email).values_list('email', flat=True)[0],
                    password=users_details.objects.filter(email=user.email).values_list('password', flat=True)[0],
                )

                u_ = user_approve.objects.latest('id').id
                u = user_approve.objects.get(id=u_)

                user.pattern = "s"
                user.save()

                null_records = user_approve.objects.filter(Q(name__isnull=True)).values_list('id', flat=True)
                null_record_ids = list(null_records)
                print('vimal:', null_record_ids)

                messages.success(request, 'You Have Logged In')
                return render(request, 'admin/admin_home.html', {'u': u})

        except:
            # increment login attempts
            user = users_details.objects.get(email=email)
            user.login_attempts += 1
            user.save()
            pat = users_details.objects.get(email=email)
            pat.pattern = "f"
            messages.success(request, "Unauthorized user name and password")
            pat.save()

            # check if login attempts have exceeded the limit
            if user.login_attempts == 5:
                user = users_details.objects.get(email=email)
                user.login_attempts = 0
                user.save()

    return render(request,'hacker/hacker_login.html')


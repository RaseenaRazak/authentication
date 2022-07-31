from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Create your views here.
from app_authproject.models import dog


def index(request):
    obj = dog.objects.all()
    return render(request,'index.html',{'result' : obj})

def register(request):
    if request.method=='POST':
        un=request.POST['username']
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        email = request.POST['email']
        pw = request.POST['password']
        cpw = request.POST['c_password']

        if pw==cpw:
            if User.objects.filter(username=un).exists():
                messages.info(request, 'username already exist')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'email already exist')
                return redirect('register')
            else:
                user=User.objects.create_user(username=un, first_name=fn, last_name=ln, email=email, password=pw)
                user.save()
                return redirect('login')
        else:
            messages.info(request,'password mismatch')


    return render(request,'register.html')

def login(request):

    if request.method == 'POST':
        un = request.POST['username']
        pw = request.POST['password']
        user=auth.authenticate(username=un, password=pw)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Invalid user')
            user.save()
            return redirect('login')

    return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

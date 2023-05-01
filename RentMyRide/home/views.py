from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from home.models import Vehicles,Dashboard
from datetime import datetime
from django.contrib import messages
from home.functions import calcCost
# username of user
userName=''
# Create your views here.
def action(request):
    return render(request, 'ActionPage.html')

@login_required(login_url='login')
def home(request):
    if request.method =='POST':
        fromDate = request.POST.get('from')
        toDate = request.POST.get('to')
        v_type = request.POST.get('vType')
        city = request.POST.get('city')
        address = request.POST.get('address')
        try:
            mycar = Vehicles.objects.get(isBooked=False , v_type=v_type,city=city)
            sr_no=mycar.id
            v_no = mycar.reg_no
            DriverName = mycar.DriverName
            DriverContact = mycar.DriverContact
            u_name = userName
            cost = calcCost(v_type)
            db = Dashboard(u_name=u_name,fromDate=fromDate,toDate=toDate,cost=cost,v_no=v_no,DriverName=DriverName,DriverContact=DriverContact,address=address,v_type=v_type)
            db.save()
            Vehicles.objects.filter(id=sr_no).update(isBooked=True)
            messages.success(request, "Your Booking is done Successfully.!")
        except:
            messages.error(request, "Sorry,Vehicle not found!")
    return render(request, 'home.html')

def signup(request):
    if request.method =='POST':
        fname=request.POST.get('fName')
        lname=request.POST.get('lName')
        email=request.POST.get('email')
        uName=email
        pass1=request.POST.get('password')
        pass2=request.POST.get('confirmPassword')
        if pass1!=pass2:
            messages.error(request, "Passwords should be same.")
        else:
            try:
                user=User.objects.create_user(uName,email,pass1)
                user.first_name = fname
                user.last_name = lname
                user.save()
                return redirect('login')
            except:
                messages.error(request, "User already Exists.!")
        

    return render(request, 'signup.html')

def loginPage(request):
    if request.method =='POST':
        uName=request.POST.get('username')
        pass1=request.POST.get('password')
        my_user=authenticate(request,username=uName,password=pass1)
        if my_user is not None:
            login(request,my_user)
            global userName
            userName= uName
            return redirect('home')
        else:
            messages.error(request, "Your Username or Password is incorrect.")


    return render(request, 'login.html')

def logoutPage(request):
    logout(request)
    global userName
    userName=''
    return redirect('action')

def register(request):
    if request.method =='POST':
        try:
            reg_no=request.POST.get('license-number')
            city = request.POST.get('city')
            v_type = request.POST.get('v-type')
            DriverName = request.POST.get('driverName')
            DriverContact =request.POST.get('driverContact')
            my_vehicle = Vehicles(reg_no=reg_no,city=city,v_type=v_type,isBooked=False,RegDate=datetime.now(),DriverName=DriverName,DriverContact=DriverContact)
            my_vehicle.save()
            messages.success(request, "Your Vehicle is Successfully Registered")
        except:
            messages.error(request, "Vehicle Already exists!")
    return render(request,'register.html')

@login_required(login_url='login')
def dashboard(request):
    bookings=Dashboard.objects.filter(u_name=userName)
    context={
        'data' : bookings
    }
    return render(request,'dashboard.html',context)

def TnC(request):
    return render(request,'TnC.html')
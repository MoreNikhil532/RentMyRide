from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from home.models import Vehicles,Dashboard
from datetime import datetime
from django.contrib import messages
from home.utils import *
import random

# username of user
userName=''
a=random.randint(1000, 9999)
# Create your views here.
def action(request):
    return render(request, 'ActionPage.html')

@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        fromDate = request.POST.get('from')
        toDate = request.POST.get('to')
        v_type = request.POST.get('vType')
        city = request.POST.get('city')
        address = request.POST.get('address')
        try:
            mycar = Vehicles.objects.filter(isBooked=False, v_type=v_type, city=city)
            mycar = mycar[0]
            sr_no = mycar.id
            v_no = mycar.reg_no
            DriverName = mycar.DriverName
            DriverContact = mycar.DriverContact
            u_name = userName
            cost = calcCost(v_type)
            db = Dashboard(u_name=u_name, fromDate=fromDate, toDate=toDate, cost=cost, v_no=v_no,
                           DriverName=DriverName, DriverContact=DriverContact, address=address, v_type=v_type)
            db.save()
            Vehicles.objects.filter(id=sr_no).update(isBooked=True)

            # Send booking confirmation email
            send_booking_confirmation_email(user=request.user, vehicle=mycar, cost=cost)

            messages.success(request, "Your Booking is done Successfully.!")
        except:
            messages.error(request, "Sorry, Vehicle not found!")

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
                send_account_creation_email(user)
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

@login_required(login_url='login')
def changePassword(request):
    user_name=request.user
    otpSent=a
    
    sub="OTP for password change @RentMyRide"
    msg=f'Dear {user_name.first_name}, \n\n\tWe have received a request to change the password for your RentMyRide account. To proceed with the password change, please use the following One-Time Password (OTP).\n\n\nOTP : {otpSent}\n\nPlease note that this OTP is valid for a short period. Do not share this OTP with anyone, including RentMyRide support.'
    uemail=user_name.username
    to=[]
    to.append(uemail)
    send_email(sub,msg,to)

    if request.method == 'POST':
        # oldPW=request.POST.get('old-password')
        newPW=request.POST.get('new-password')
        confirmPW=request.POST.get('confirm-password')
        otp=request.POST.get('otp')
        otp=int(otp)
        user=User.objects.get(username=uemail)
        
        if check(otp,otpSent)==True:
            try:
                if newPW != confirmPW:
                    messages.error(request, "Both passwords should be same")
                else:
                    user.set_password(newPW)
                    user.save()
                    messages.success(request, "Your Password has been Changed Successfully")
                    return redirect('login')
            except:
                messages.error(request, "Something went Wrong!")
        else:
            messages.error(request, "OTP is incorrect!")

    return render(request,'changePassword.html')

@login_required(login_url='login')
def delete_account(request):
    user = request.user

    if 'otp_sent' not in request.session:
        otp_sent = generate_otp()
        request.session['otp_sent'] = otp_sent
        send_otp_verification_email(user, otp_sent)

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')

        if entered_otp == request.session.get('otp_sent'):
            send_account_deletion_email(user)
            del request.session['otp_sent']
            user.delete()
            messages.success(request, "Your account has been successfully deleted.")
            return redirect('action')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'delete_account.html', {'user': user})

def TnC(request):
    return render(request,'TnC.html')

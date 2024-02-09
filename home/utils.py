from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from datetime import datetime 
from .models import Vehicles
import random

def calcCost(type):
    if type=="Sedan":
        return 750
    elif type=="Hatchback":
        return 500
    elif type=="Suv":
        return 1000
    elif type=="Electric car":
        return 650
    elif type=="Motorcycle":
        return 250
    elif type=="Moped":
        return 250
    elif type=="Electric Bike":
        return 300
    elif type=="Traveller Van":
        return 2500

def send_email(sub,msg,to):
    subject = sub
    message = msg
    email_from = settings.EMAIL_HOST_USER
    recipient_list = to
    send_mail( subject, message, email_from, recipient_list )
    
def check(a,b):
    if a==b:
        return True
    else:
        return 
    
def send_booking_confirmation_email(user_name, vehicle, cost):
    sub = "Successful Vehicle Booking Confirmation @RentMyRide"
    msg = f"\n\nDear {user_name.first_name},\n\n" \
          f"Congratulations! Your vehicle booking on RentMyRide has been successfully confirmed. Here are the details of your booking:\n\n" \
          f"- Vehicle: {vehicle.reg_no}\n" \
          f"- Pickup Date and Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n" \
          f"- Return Date and Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n" \
          f"- Total Cost: {cost}\n\n" \
          f"Thank you for choosing RentMyRide for your transportation needs. We hope you have a fantastic experience with the booked vehicle.\n\n" \
          f"If you have any questions or need further assistance, feel free to reach out to our customer support team.\n\n" \
          f"Safe travels!\n\n" \
          f"Best regards,\nRentMyRide Team"

    uemail = user_name.username
    to = [uemail]
    send_email(sub, msg, to)

def send_account_creation_email(user_name, user_email):
    subject = 'Welcome to RentMyRide!'
    message = f'Dear {user_name.first_name},\n\nWelcome to RentMyRide! We are thrilled to have you on board. Your account has been created successfully. Explore our platform to find the perfect vehicle for your needs.\n\nThank you for choosing RentMyRide!\n\nBest regards,\nThe RentMyRide Team'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)

def generate_otp():
    return str(random.randint(1000, 9999))

def send_otp_verification_email(user_name, user_email, otp_sent):
    subject = 'OTP for Account Deletion Verification'
    message = f'Dear {user_name.first_name},\n\nTo verify your identity and proceed with the account deletion process, please enter the following One-Time Password (OTP):\n\nOTP: {otp_sent}\n\nThis OTP is valid for a short period. Do not share it with anyone.\n\nBest regards,\nThe RentMyRide Team'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)

def send_account_deletion_email(user_name, user_email):
    subject = 'Account Deletion Confirmation'
    message = f'Dear {user_name.first_name},\n\nWe regret to inform you that your RentMyRide account has been successfully deleted. If you did not initiate this action, please contact our support team.\n\nThank you for being a part of RentMyRide.\n\nBest regards,\nThe RentMyRide Team'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)
from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
import asyncio
from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib.auth import logout as auth_logout

import uuid
from django.core.mail import send_mail

# Create your views here.

def registration(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        print(f'fname: {fname},lname: {lname}, email: {email}, password1: {password1}, '
              f'password2: {password2}')


        # Validate password length
        if len(password1) < 8:
            messages.warning(request, 'Both passwords must be at least 8 characters long.')
            return render(request, 'Auth/registration.html', {
                'fname': fname,
                'lname': lname,
                'email': email,

            })

        if password1 != password2:
            messages.warning(request, 'Passwords do not match.')
            return render(request, 'Auth/registration.html', {
                'fname': fname,
                'lname': lname,
                'email': email,

            })


        # if CustomUser.objects.filter(fname=fname).exists():
        #     messages.warning(request, 'Username already exists. Please choose a different username.')
        #     return redirect('registration')

        if User.objects.filter(email=email).exists():
            messages.warning(request, 'An account with this email already exists. Please use a different email.')
            return redirect('registration')


        user = User.objects.create_user(
            username=email,
            first_name=fname,
            last_name=lname,
            email=email,
            password=password1,
        )
        user.save()

        messages.success(request, "Account created successfully! You can now log in.")
        return redirect('login')


    return render(request, 'Auth/registration.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        print(f"Remember Me: {remember_me}")


        user = authenticate(username=email, password=password)

        if user is not None:
            auth_login(request, user)

            if remember_me:
                request.session.set_expiry(10800)  # 3 hour
            else:
                request.session.set_expiry(0)

            messages.success(request, "You are successfully logged in!")
            return redirect('home')
        else:
            messages.warning(request, "Invalid email or password!")
            return render(request, 'Auth/login.html', {
                'email': email,
            })

    return render(request, 'Auth/login.html')


def custom_logout(request):
    auth_logout(request)
    messages.success(request, "User logged out!")
    return redirect('login')


def forgetpassword(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            user = User.objects.get(email=email)
            if not user:
                messages.warning(request, "No User Found!")
                return redirect('ForgetPassword')

            forget_password_token = str(uuid.uuid4())

            # Check if Profile object exists for the user
            try:
                prof_obj = Profile.objects.get(user=user)
                prof_obj.forget_password_token = forget_password_token
            except Profile.DoesNotExist as e:
                print(e)
                prof_obj = Profile(user=user, forget_password_token=forget_password_token)

            prof_obj.save()
            asyncio.run(send_forget_password_mail(email, forget_password_token, request))
            return render(request, 'Auth/mail_success.html')

    except User.DoesNotExist:
        messages.warning(request, "No User Found!")
    except Exception as e:
        print(e)

    return render(request, 'Auth/forget.html', locals())


async def send_forget_password_mail(email, token, request):
    subject = 'Your Forget Password Link'
    message = f' Hi, click on the link to reset your password {request.scheme}://{request.META["HTTP_HOST"]}/change_password/{token}'
    sender = settings.EMAIL_HOST_USER
    receiver = [email]
    await sync_to_async(send_mail)(subject, message, sender, receiver)


def verify(request, forget_password_token):
    prof_obj = Profile.objects.filter(forget_password_token=forget_password_token).first()
    prof_obj.is_verified = True
    return redirect('login')

def change_password(request, token):
    try:
        prof_obj = Profile.objects.filter(forget_password_token=token).first()
        if not prof_obj:
            messages.warning(request, "Invalid or expired token!")
            return redirect('forgetpassword')

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if not new_password or not confirm_password:
                messages.warning(request, "Please fill out all fields!")
                return redirect(f'/change_password/{token}/')

            if new_password != confirm_password:
                messages.warning(request, "Passwords do not match!")
                return redirect(f'/change_password/{token}/')

            user = prof_obj.user
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password changed successfully!")
            return redirect('login')

        return render(request, 'Auth/pass_change.html', {'user_id': prof_obj.user.id})

    except Exception as e:
        print(e)
        messages.error(request, "An error occurred. Please try again.")
        return redirect('forgetpassword')

from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
import allauth
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
import json

fs = FileSystemStorage()

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        cuser = request.user
        if cuser.first_name == '' or cuser.last_name == '' or cuser.email == '' or not cuser.has_usable_password():
            if request.user.has_usable_password():
                pset = False
            else:
                pset = True 
            User = get_user_model()
            users = User.objects.all().values('username')
            userlist = []
            for aus in users:
                laus = list(aus.values())
                userlist.append(laus[0])

            return render(request, 'web/complete_profile.html', {
                "pset":pset,
                # "allusers":users,
                "userlist":userlist,
            })
        else:
            return render(request, 'web/homepage.html')
    else:
        return redirect('account_login')

def complete_profile(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            cuser = request.user
            fn = request.POST['fname']
            ln = request.POST['lname']
            us = request.POST['username']
            if not request.user.has_usable_password():
                p1 = request.POST['password']
                p2 = request.POST['password1']
                cuser.set_password(p1)  
            cuser.first_name = fn
            cuser.last_name = ln
            cuser.username = us
            cuser.save()
            return redirect('Home')
        else:
            redirect('account_login')
    else:
        return redirect('account_login')

def update_basic_info(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            cuser = request.user
            fn = request.POST['fname']
            ln = request.POST['lname']
            us = request.POST['username']
            cuser.first_name = fn
            cuser.last_name = ln
            cuser.username = us
            cuser.save()
            messages.success(request, 'Successfully Changed Details')
            return redirect('profile')
        else:
            messages.danger(request, 'Successfully Changed Details')
            return redirect('profile')
    else:
        return redirect('account_login')

def update_other_info(request):
    pass

def profile(request):
    User = get_user_model()
    users = User.objects.all().values('username')
    userlist = []
    for aus in users:
        laus = list(aus.values())
        userlist.append(laus[0])
    if fs.exists(request.user.email+"_pic.jpeg"):
        dp = True
    else:
        dp = False
    return render(request, 'web/view_profile.html',{
        "userlist":userlist,
        "dp_exists":dp,
    })


def view_profile(request, uname):
    return HttpResponse(f"Profile of {uname}")

def check_username_availability(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data['username']
        User = get_user_model()
        if User.objects.all().filter(username=username).exists():
            return JsonResponse({'username_error':'This username is already taken'})
        return JsonResponse({'username_available':True})

def upload_img(request):
    if request.method == "POST":
        # img = request.POST['new_image']
        new_profile_pic = request.FILES['new_image']
        if fs.exists(request.user.email+"_pic.jpeg"):
            fs.delete(request.user.email+"_pic.jpeg")
        fs.save(request.user.email+"_pic.jpeg", new_profile_pic)
        # return HttpResponse(f'Profile of  <img src="/">')
        return redirect('profile')

def remove_profile(request):
    if request.method == "POST":
        if fs.exists(request.user.email+"_pic.jpeg"):
            fs.delete(request.user.email+"_pic.jpeg")
            
        return redirect('profile')
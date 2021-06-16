from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
import allauth
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .models import UserInfo
from django.http import JsonResponse
import json
import os

User = get_user_model()
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
        messages.error(request, 'You must login to continue')
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
            messages.warning(request, 'Successfully Changed Details')
            return redirect('profile')
    else:
        return redirect('account_login')

def update_other_info(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            cuser = request.user
            abt = request.POST['about']
            ldnurl = request.POST['linkedinurl']
            stpr = request.POST['storprof']
            plow = request.POST['placeofwork']
            gradyr = request.POST['gradyear']
            # print('\n****** DETAILS  ******\n ', abt,' ', ldnurl,' ', stpr,' ', plow,' ', gradyr)
            messages.success(request,'Your Changes has been successfully saved')
            if UserInfo.objects.all().filter(uname = cuser).exists():
                cuserinfo = UserInfo.objects.all().filter(uname = cuser)
                cuserinfo = cuserinfo[0]
                cuserinfo.about = abt
                cuserinfo.linkedin = ldnurl
                cuserinfo.storprof = stpr.capitalize()
                cuserinfo.where_do_you_work = plow
                cuserinfo.graduation_year = gradyr
                cuserinfo.save()
                return redirect('profile')
            else:
                cuserinfo = UserInfo(uname=cuser, about=abt, linkedin=ldnurl, storprof=stpr, where_do_you_work=plow, graduation_year=gradyr)
                cuserinfo.save()
                return redirect('profile')
        else:
            messages.error(request,'Invalid Attempt, Please try again !!')
            return redirect('profile')
    else:
        messages.error(request, 'Invalid Attempt, Login To Continue')
        return redirect('account_login')


def profile(request):
    if request.user.is_authenticated:
        users = User.objects.all().values('username')
        userlist = []
        for aus in users:
            laus = list(aus.values())
            userlist.append(laus[0])
        if fs.exists(request.user.email+"_pic.jpeg"):
            dp = True
        else:
            dp = False
        return render(request, 'web/edit_profile.html',{
            "dp_exists":dp,
        })
    else:
        messages.error(request, 'You must login to view profile')
        return redirect('account_login')


def view_profile(request, uname):
    if request.user.is_authenticated:
        if User.objects.all().filter(username=uname).exists():
            user_to_view = User.objects.all().get(username=uname)
            if fs.exists(user_to_view.email+"_pic.jpeg"):
                dp = True
            else:
                dp = False
            return render(request, 'web/view_profile.html',{
                "dp_exists":dp,
                "cuser":user_to_view,
            })
        else:
            messages.error(request, 'No such User Exists')
            return redirect('Home')
    else:
        messages.error(request, 'You must login to view profile')
        return redirect('account_login')
        
def check_username_availability(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data['username']
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
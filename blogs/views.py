from django.shortcuts import render, HttpResponse, redirect

# Create your views here.


def blogHome(request):
    return HttpResponse("Welcome To Blog Home")
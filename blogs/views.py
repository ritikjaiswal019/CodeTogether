from django.shortcuts import render, HttpResponse, redirect

# Create your views here.


def blogHome(request):
    return render(request, 'blogs/index.html')